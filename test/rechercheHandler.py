#-*- coding: utf-8 -*-
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.db import cDb
from resources.lib.util import cUtil

import os
import urllib
import xbmcgui
import xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.test.util import VSlog,VStranslatePathAddon,VSgetsetting,VSlang,VScreateDialog,VSupdateDialogSearch,VSfinishDialog

bFolder = VStranslatePathAddon("path") + '/resources/sites/'

class cRechercheHandler:

    def __init__(self):
        self.__sText = ""
        self.__sDisp = ""
        self.__sRead = "True"

    def setText(self, sText):
        if not sText:
            oGui = cGui()
            sSearchText = oGui.showKeyBoard()
            sText = urllib.quote(sSearchText)
        self.__sText = sText
        return self.__sText

    def getText(self):
        return self.__sText

    def setRead(self, sRead):
        self.__sRead = sRead

    def getDisp(self):
        return self.__sDisp
        
    def setDisp(self, sDisp):
        if not sDisp:
            disp = ['search1','search2','search3','search4','search5','search10']
            dialog2 = xbmcgui.Dialog()
            dialog_sel = [VSgetsetting('search1_label'),VSgetsetting('search2_label'),VSgetsetting('search3_label'),VSgetsetting('search4_label'),VSlang(30092),VSlang(30417)]

            ret = dialog2.sel(VSlang(30093),dialog_sel)

            if ret > -1:
                sDisp = disp[ret]
 
        self.__sDisp = sDisp
        
        return self.__sDisp

    def __getFileNamesFromFolder(self, sFolder):
        aNameList = []
        #items = os.listdir(sFolder)
        items = os.listdir(unicode(sFolder, 'utf-8'))

        for sItemName in items:
            #sFilePath = os.path.join(sFolder, sItemName)
            sFilePath = os.path.join(unicode(sFolder, 'utf-8'), sItemName)
            # xbox hack
            sFilePath = sFilePath.replace('\\', '/')

            if (os.path.isdir(sFilePath) == False):
                #if (str(sFilePath.lower()).endswith('py')):
                if (sFilePath.lower().endswith('py')):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
        return aNameList

    def getAvailablePlugins(self):
        oConfig = cConfig()
        sText = self.getText()
        if not sText:
            return False
        sLabel = self.getDisp()
        if not sLabel:
            return False

        #historique
        try:
            if (VSgetsetting("history-view") == 'true' and self.__sRead != "False"):
                meta = {}
                meta['title'] = sText
                meta['disp'] = sLabel
                cDb().insert_history(meta)
        except: 
            pass

        # xbox hack
        sFolder = bFolder.replace('\\', '/')
        VSlog("Sites Folder: " + sFolder)

        aFileNames = self.__getFileNamesFromFolder(sFolder)
  
        aPlugins = []
        for sFileName in aFileNames:
            aPlugin = self.__importPlugin(sFileName, sLabel)
            if aPlugin:
                aPlugins.append(aPlugin)
        
        #multiselect
        if sLabel == 'search5':
            multi = []
            for plugin in aPlugins:
                multi.append(plugin['identifier'])
            dialog = xbmcgui.Dialog()
            ret = dialog.multiselect(VSlang(30094), multi)
            NewFileNames = []
            if ret > -1:
                for i in ret:
                    NewFileNames.append(aPlugins[i])

            aPlugins = NewFileNames
        #fin multiselect
        return aPlugins
        
    def __importPlugin(self, sName, sLabel):
        pluginData = {}
        sPluginSettingsName = sLabel+'_' +sName
        bPlugin = VSgetsetting(sPluginSettingsName)
        #multicherche
        if sLabel == 'search5':
            bPlugin = 'true'

        OnPlugins = VSgetsetting('plugin_' + sName)

        if (bPlugin == 'true') and (OnPlugins == 'true'):
            try:

                plugin = __import__('resources.sites.%s' % sName, fromlist=[sName])
                
                pluginData['identifier'] = plugin.SITE_IDENTIFIER
                pluginData['name'] = plugin.SITE_NAME
                pluginData['search'] = plugin.URL_SEARCH

            except Exception, e:
                VSlog("cant import plugin: " + str(sName))
            
        return pluginData
        
    def searchGlobal(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        sSearchText = oInputParameterHandler.getValue('searchtext')
        sReadDB = oInputParameterHandler.getValue('readdb')
        sDisp = oInputParameterHandler.getValue('disp')

        sSearchText = self.setText(sSearchText)
        self.setDisp(sDisp)
        self.setRead(sReadDB)
        aPlugins = self.getAvailablePlugins()
        if not aPlugins: 
            return True
        total = len(aPlugins)
    
        #xbmc.log(str(aPlugins), xbmc.LOGNOTICE)
    
        dialog = VScreateDialog("vStream")
        xbmcgui.Window(10101).setProperty('search', 'true')
    
        oGui.addText('globalSearch', '[COLOR khaki]%s: %s[/COLOR]' % (VSlang(30076), sSearchText), 'none.png')
    
        for count, plugin in enumerate(aPlugins):
    
            text = '%s/%s - %s' % ((count+1), total, plugin['name'])
            VSupdateDialogSearch(dialog, total, text)
            if dialog.iscanceled():
                break
        
            #nom du site
            oGui.addText(plugin['identifier'], '%s. [COLOR olive]%s[/COLOR]' % ((count+1), plugin['name']), 'sites/%s.png' % (plugin['identifier']))
            #recherche import
            self.pluginSearch(plugin, sSearchText)
      
        xbmcgui.Window(10101).setProperty('search', 'false')
    
        #affichage
        total=len(oGui.searchResults)
        #filtre
        int_1 = cUtil().CheckOrd(sSearchText)
    
        for count,result in enumerate(oGui.searchResults):
            text = '%s/%s - %s' % ((count+1/total), total, result['guiElement'].getTitle())
            VSupdateDialogSearch(dialog, total, text)
        
            #filtre
            if VSgetsetting('search_filter') == 'true' and result['guiElement'].getFunction() != 'DoNothing':
                int_2 = cUtil().CheckOrd(result['guiElement'].getFileName())
                middle = int(abs(int_1-int_2))
                #xbmc.log('%s (%s) - %s (%s)' % (middle, result['guiElement'].getFileName(), cConfig().getSetting('search_ord'), sSearchText),  xbmc.LOGNOTICE)
                if middle > int(VSgetsetting('search_ord')):
                    continue
            
            
            oGui.addFolder(result['guiElement'],result['params'])
            #xbmc.log('%s - %s' % (middle,old_label),  xbmc.LOGNOTICE)
        
        VSfinishDialog(dialog)
    

        oGui.setEndOfDirectory()

        return True
    
    def pluginSearch(self,plugin, sSearchText):
        try:
            plugins = __import__('resources.sites.%s' % plugin['identifier'], fromlist=[plugin['identifier']])
            function = getattr(plugins, plugin['search'][1])
            sUrl = plugin['search'][0]+str(sSearchText)
            function(sUrl)      
            VSlog("Load Recherche: " + str(plugin['identifier']))
        except:
            VSlog(plugin['identifier']+': search failed')

            
