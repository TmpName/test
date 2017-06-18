#-*- coding: utf-8 -*-
#https://github.com/Kodi-vStream/venom-xbmc-addons
#nom du site ,fonction , nom , thumb , fanart, le reste
#beaucoup plus simple d'avoir des dossiers spécifique
from resources.test.util import VSlog,VStranslatePathAddon,VSlang
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
import xbmc
import xbmcgui
import xbmcplugin
import sys

path = VStranslatePathAddon("path") + '/resources/art/'

Pluginurl = sys.argv[0]

Pluginhandle = int(sys.argv[1])

class cGui():

    #affiche les dossiers simple
    #multi site - multi fonction
    def addSimpleFolder(self, olist):

        listing = []
        for aEntry in olist:

            list_item = xbmcgui.ListItem(label=aEntry[2])

            list_item.setArt({'thumb': path+aEntry[3],'icon': path+aEntry[3],'fanart': path+aEntry[4]})
            
            list_item.addContextMenuItems(self.defaultContext())
            
            url = self.CreateUrl(aEntry[0], aEntry[1], aEntry[2], aEntry[3], aEntry[4], aEntry[5])

            listing.append((url, list_item, True))

        xbmcplugin.addDirectoryItems(Pluginhandle, listing, len(listing))
        
    #affiche les dossiers historique de recherche
    #menu context spécifique pour chaque entrée
    def addHistoryFolder(self, olist):
    
        listing = []
        for aEntry in olist:

            list_item = xbmcgui.ListItem(label=aEntry[2])

            list_item.setArt({'thumb': path+aEntry[3],'icon': path+aEntry[3],'fanart': path+aEntry[4]})
            
            list_item.addContextMenuItems([(VSlang(30412), 'XBMC.RunPlugin('+Pluginurl+'?site=cHome&function=delSearch&searchtext='+aEntry[2]+')')])

            url = self.CreateUrl(aEntry[0], aEntry[1], aEntry[2], aEntry[3], aEntry[4], aEntry[5])

            listing.append((url, list_item, True))

        xbmcplugin.addDirectoryItems(Pluginhandle, listing, len(listing))
        
    #affiche les dossiers genres
    #oGui.addGenreFolder(SITE_IDENTIFIER,'showMovies',liste)
    #meme site meme function donc    
    def addGenreFolder(self, Site, Function, olist):
        oInputParameterHandler = cInputParameterHandler()
        sFanart = oInputParameterHandler.getValue('fanart')

        listing = []
        for aEntry in olist:

            list_item = xbmcgui.ListItem(label=aEntry[0])

            list_item.setArt({'thumb': path+'genres.png','icon': path+'genres.png','fanart': path+sFanart})
            
            list_item.addContextMenuItems(self.defaultContext())

            url = url = self.CreateUrl(Site, Function, aEntry[0],'genres.png',sFanart,'siteUrl='+aEntry[1])

            listing.append((url, list_item, True))

        xbmcplugin.addDirectoryItems(Pluginhandle, listing, len(listing))
        
    
    def defaultContext(self):
        context = []
        context.append((VSlang(30023), 'XBMC.RunPlugin('+Pluginurl+'?site=globalParametre&function=opensetting)'))
        context.append((VSlang(30210), 'XBMC.Container.Update('+Pluginurl+'?site=cFav&function=getFavourites)'))
        return context
        
    def CreateUrl(self,Site,Function,Title,Thumb,Fanart,Siteurl):
        #retourne l'url final
        return '%s?site=%s&function=%s&title=%s&thumb=%s&fanart=%s&%s' % (Pluginurl, Site, Function, Title, Thumb, Fanart, Siteurl)   
        
        
    def endOfDirectory(self):
        xbmcplugin.addSortMethod(Pluginhandle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(Pluginhandle,True,cacheToDisc=True) #cache pas vraiment nécessaire    
        
