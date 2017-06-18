#-*- coding: utf-8 -*-
#https://github.com/Kodi-vStream/venom-xbmc-addons
#Venom

#test
from resources.test.home import cHome
from resources.test.siteHandler import cSiteHandler
from resources.test.util import VSlog


#officiel
from resources.lib.gui.gui import cGui
from resources.lib.db import cDb
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.gui.hoster import cHosterGui
import xbmcaddon,xbmcgui,xbmc
from resources.lib.about import cAbout

class main:
    def __init__(self):
        self.parseUrl()
        cDb()._create_tables()
        
    def parseUrl(self):

        oInputParameterHandler = cInputParameterHandler()
        # params = oInputParameterHandler.getAllParameter()
        # VSlog(params)

        
        if (oInputParameterHandler.exist('function') and oInputParameterHandler.exist('site')):
            sFunction = oInputParameterHandler.getValue('function')
            sSiteName = oInputParameterHandler.getValue('site')
            
            if (sFunction == 'DoNothing'):
                return 
                
            VSlog('load site ' + sSiteName + ' and call function ' + sFunction)
            
            #home
            if (sSiteName == 'cHome'):
                oHome = cHome()
                exec "oHome."+ sFunction +"()"
                
            #librairie
            elif (sSiteName == 'cLibrary'):
                from resources.lib.library import cLibrary
                oLibrary = cLibrary()
                exec "oLibrary."+ sFunction +"()"
                
            #marque page   
            elif (sSiteName == 'cFav'):
                from resources.lib.favourite import cFav
                oFav = cFav()
                exec "oFav."+ sFunction +"()"
                
            #dl    
            elif (sSiteName == 'cDownload'):
                from resources.lib.download import cDownload
                oDownload = cDownload()
                exec "oDownload."+ sFunction +"()"
                
            #sous menu home vers sources  
            elif (sSiteName == 'sitehandler' and sFunction == 'callplugin'):
                oSiteHandler = cSiteHandler()
                oSiteHandler.callplugin()
                
            #trakt    
            elif (sSiteName == 'cTrakt'):
                from resources.lib.trakt import cTrakt
                oTrakt = cTrakt()
                exec "oTrakt."+ sFunction +"()"
                
            #hoster    
            elif (sSiteName == 'cHosterGui'):
                oHosterGui = cHosterGui()
                exec "oHosterGui."+ sFunction +"()"
                
            #gui    
            elif (sSiteName == 'cGui'):
                oGui = cGui()
                exec "oGui."+ sFunction +"()"
                
            #parametres de vstream   
            elif (sSiteName == 'globalParametre'):
                xbmcaddon.Addon('plugin.video.vstream').openSettings()
                xbmc.executebuiltin("Container.Refresh")
                
            #toutes les sources     
            elif (sSiteName == 'globalSources'):
                oSiteHandler = cSiteHandler()
                oSiteHandler.callAllSources()
                
            #recherche global    
            elif (sSiteName == 'globalSearch'):
                from resources.test.rechercheHandler import cRechercheHandler
                oTr = cRechercheHandler()
                oTr.searchGlobal()

                
            #mise a jour    
            elif (sSiteName == 'MAJ'):
                try:
                    oAbout = cAbout()
                    oAbout.checkdownload()
                except:
                   pass
            else:
                try:
                   plugins = __import__('resources.sites.%s' % sSiteName, fromlist=[sSiteName])
                   function = getattr(plugins, sFunction)
                   function()
                except Exception as e:
                    VSlog('could not load site: ' + sSiteName + ' error: ' + str(e))
                    return
                    
                VSlog('load >>>>>>>>>>>>>>>>>>>>>> site ')


        else:
            #si aucun argument verif mise a jour et on load home
            try:
                oAbout = cAbout()
                oAbout.getUpdate()
            except Exception as e:
                #VSlog(e)
                pass
                
            oHome = cHome()    
            oHome.load()
            
            VSlog('load >>>>>>>>>>>>>>>>>>> home ')
            
main()
