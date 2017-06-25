#-*- coding: utf-8 -*-
#https://github.com/Kodi-vStream/venom-xbmc-addons

# site fonction name thumb fanart "siteUrl=http://venom"
# sous menu page home + toutes les sources
# combinaison et modif sitehandler pluginhandler
from resources.test.util import VSlog,VStranslatePathAddon,VSgetsetting
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.test.gui import cGui
import os

bFolder = VStranslatePathAddon("path") + '/resources/sites/'

class cSiteHandler:

    def __getFileNamesFromFolder(self, sFolder):
        aNameList = []

        items = os.listdir(sFolder)
        items.sort()
        for sItemName in items:

            sFilePath = os.path.join(sFolder, sItemName)

            sFilePath = sFilePath.replace('\\', '/')
            
            if (os.path.isdir(sFilePath) == False):
                if (sFilePath.lower().endswith('py')):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
                    
        return aNameList
        
    #sous menus page home
    def __importPlugin(self, sName, sLabel):
        try:
            plugin = __import__('resources.sites.%s' % sName, fromlist=[sName])
            sSearch = getattr(plugin, sLabel)
            sSiteName = getattr(plugin, "SITE_NAME")

            sPluginSettingsName = 'plugin_' + sName
            return sSearch[0], sPluginSettingsName, sSearch[1], sSiteName
        except Exception, e:
            return False, False

    def getAvailablePlugins(self, sLabel,sFanart):
      
        sFolder = bFolder.replace('\\', '/')

        aFileNames = self.__getFileNamesFromFolder(sFolder)
        
        aPlugins = []
        for sFileName in aFileNames:

            aPlugin = self.__importPlugin(sFileName, sLabel)

            if (aPlugin[0] != False):
                sSiteUrl = aPlugin[0]
                sPluginSettingsName = aPlugin[1]
                sSiteFunc = aPlugin[2]
                sSiteName = aPlugin[3]
                sSiteIcon = 'sites/%s.png' % (sFileName)

                bPlugin = VSgetsetting(sPluginSettingsName)
                if (bPlugin != ''):
                    if (bPlugin == 'true'):
                        aPlugins.append((sFileName,sSiteFunc,sSiteName,sSiteIcon,sFanart,'siteUrl='+str(sSiteUrl)+''))
                else:
                    aPlugins.append((sFileName,sSiteFunc,sSiteName,sSiteIcon,sFanart,'siteUrl='+str(sSiteUrl)+''))


        return aPlugins
        
    def callplugin(self):
        oGui = cGui()
        
        oInputParameterHandler = cInputParameterHandler()
        sSiteUrl = oInputParameterHandler.getValue('siteUrl')
        sFanart = oInputParameterHandler.getValue('fanart')
        
        aPlugins = self.getAvailablePlugins(sSiteUrl,sFanart)

        oGui.FolderType1(aPlugins)
        oGui.endOfDirectory()
        
    #toutes les sources
    def callAllSources(self):
        oGui = cGui()
        
        aPlugins = self.getAllSources()

        oGui.FolderType1(aPlugins)
        oGui.endOfDirectory()
        
    def getAllSources(self):
     
        sFolder = bFolder.replace('\\', '/')

        aFileNames = self.__getFileNamesFromFolder(sFolder)

        aPlugins = []
        for sFileName in aFileNames:

            aPlugin = self.__importAllSources(sFileName)

            if (aPlugin[0] != False):
                sSiteName = aPlugin[0]
                sPluginSettingsName = aPlugin[1]
                sSiteIcon = 'sites/%s.png' % (sFileName)
                sFanart = 'host_fanart.jpg'
                
                bPlugin = VSgetsetting(sPluginSettingsName)
                if (bPlugin != ''):
                    if (bPlugin == 'true'):
                        aPlugins.append((sFileName,'load',sSiteName,sSiteIcon,sFanart,'siteUrl=http://venom'))
                else:
                    aPlugins.append((sFileName,'load',sSiteName,sSiteIcon,sFanart,'siteUrl=http://venom'))

        return aPlugins

    def __importAllSources(self, sName):
        try:
            plugin = __import__('resources.sites.%s' % sName, fromlist=[sName])
            
            sSiteName = getattr(plugin, "SITE_NAME")
            sPluginSettingsName = 'plugin_' + sName
            
            return sSiteName, sPluginSettingsName
        except Exception, e:
            return False, False
            
