#-*- coding: utf-8 -*-
#https://github.com/Kodi-vStream/venom-xbmc-addons
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import sys

COUNT = 0
DIALOG2 = None
    
# 14062017 test ok
def isKrypton():
    try: 
        version = xbmc.getInfoLabel('system.buildversion')
        if version[0:2] >= "17":
            return True  
        else:
            return False
    except:
        return False

def VSlog(e):
    xbmc.log('\t[PLUGIN] Vstream: '+str(e), xbmc.LOGNOTICE)
    
def VSgetsetting(label):
    return xbmcplugin.getSetting(int(sys.argv[1]), label) 

def VSsetsetting(label,value):
    return xbmcplugin.setSetting(int(sys.argv[1]), label, value)
 
def VSlang(lang):
    #util.VSgetlanguage(30003)
    return xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getLocalizedString(lang))
 
def VStranslatePathAddon(location):
    #location = (author,changelog,description,disclaimer,fanart,icon,id,name,path,profile,stars,summary,type,version)
    #util.VStranslatePathAddon("profile")
    return xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo(location))
    
def VScreateDialog(sSite):
    global DIALOG2
    if DIALOG2 == None:
        oDialog = xbmcgui.DialogProgress()
        oDialog.create(sSite)
        DIALOG2 = oDialog
        return oDialog
    else:
        return DIALOG2

def VSupdateDialog(dialog,total):
    if xbmcgui.Window(10101).getProperty('search') != 'true':
       global COUNT
       COUNT += 1
       iPercent = int(float(COUNT * 100) / total)
       dialog.update(iPercent, 'Chargement: '+str(COUNT)+'/'+str(total))
       
def VSupdateDialogSearch(dialog, total, site):
    global COUNT
    COUNT += 1
    iPercent = int(float(COUNT * 100) / total)
    dialog.update(iPercent, 'Chargement: '+str(site))

def VSfinishDialog(dialog):
    if xbmcgui.Window(10101).getProperty('search') != 'true':
       dialog.close()
       del dialog

def VScreateDialogOK(label):
    oDialog = xbmcgui.Dialog()
    oDialog.ok('vStream', label)  
    return oDialog
    
def VSerror(e):
    sIcon = VStranslatePathAddon("path") + '/resources/art/icon.png'
    xbmcgui.Dialog().notification('Vstream','Erreur: '+str(e),sIcon,2000)
    VSlog('Erreur: ' + str(e))
    
def VSshowInfo(sTitle, sDescription, iSeconds=0,sound = True):
    sIcon = VStranslatePathAddon("path") + '/resources/art/icon.png'
    if (iSeconds == 0):
        iSeconds = 1000
    else:
        iSeconds = iSeconds * 1000

    xbmcgui.Dialog().notification(str(sTitle), str(sDescription),sIcon,iSeconds,sound)
