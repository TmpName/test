#-*- coding: utf-8 -*-
#https://github.com/Kodi-vStream/venom-xbmc-addons
#nom du site ,fonction , nom , thumb , fanart, le reste

#repet folder nécessaire pour prendre en compte toutes les variantes
#gagnant au final moins de texte, moins d'icones en doublon, etc.. 

from resources.test.util import VSlog,VStranslatePathAddon,VSlang,isKrypton
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
import xbmc
import xbmcgui
import xbmcplugin
import sys

path = VStranslatePathAddon("path") + '/resources/art/'

Pluginurl = sys.argv[0]

Pluginhandle = int(sys.argv[1])

class cGui():
    
    #dossiers simple liste complete - menu context de base ou context de l'historique
    #multi site - multi fonction multi etc...
    def FolderType1(self, Olist, History=False):
    
        Context = self.defaultContext()
        Listing = []
        for aEntry in Olist:

            list_item = xbmcgui.ListItem(label=aEntry[2])

            list_item.setArt({'thumb': path+aEntry[3],'icon': path+aEntry[3],'fanart': path+aEntry[4]})
            
            if (History == False):
                list_item.addContextMenuItems(Context)
            else:
                list_item.addContextMenuItems([(VSlang(30412), 'XBMC.RunPlugin('+Pluginurl+'?site=cHome&function=delSearch&searchtext='+aEntry[2]+')')])
                
            Url = self.CreateUrl(aEntry[0], aEntry[1], aEntry[2], aEntry[3], aEntry[4], aEntry[5])

            Listing.append((Url, list_item, True))

        xbmcplugin.addDirectoryItems(Pluginhandle, Listing, len(Listing))
        
    #sous menu home uniquement pour le moment (evite repetion de texte dans home)
    def FolderType2(self, Site, Function, Fanart, olist):
    
        Context = self.defaultContext()
        listing = []
        for aEntry in olist:

            list_item = xbmcgui.ListItem(label=aEntry[0])

            list_item.setArt({'thumb': path+aEntry[1],'icon': path+aEntry[1],'fanart': path+Fanart})
            
            list_item.addContextMenuItems(Context)

            url = self.CreateUrl(Site, Function, aEntry[0], aEntry[1], Fanart, 'siteUrl='+aEntry[2])

            listing.append((url, list_item, True))

        xbmcplugin.addDirectoryItems(Pluginhandle, listing, len(listing))
        
    #pour genre ,annee etc... site , fonction, thumb, fanart, une liste(Nom,Url) #voir exemple.py
    def FolderType3(self, Site, Function, Thumb, Fanart, olist):
        
        Context = self.defaultContext()
        listing = []
        for aEntry in olist:

            list_item = xbmcgui.ListItem(label=aEntry[0])

            list_item.setArt({'thumb': path+Thumb,'icon': path+Thumb,'fanart': path+Fanart})
   
            list_item.addContextMenuItems(Context)

            url = CreateUrl(Site, Function, aEntry[0], Thumb, Fanart, 'siteUrl='+str(aEntry[1]))

            listing.append((url, list_item, True))

        xbmcplugin.addDirectoryItems(Pluginhandle, listing, len(listing))
        
    
    def defaultContext(self):
        Context = []
        if (isKrypton() == True):
            Context.append((VSlang(30023), 'XBMC.RunPlugin('+Pluginurl+'?site=globalParametre&function=opensetting)'))
            Context.append((VSlang(30210), 'XBMC.Container.Update('+Pluginurl+'?site=cFav&function=getFavourites)'))
        else:
            Context.append((VSlang(30210), 'XBMC.Container.Update('+Pluginurl+'?site=cFav&function=getFavourites)'))
            
        return Context
        
    def CreateUrl(self,Site,Function,Title,Thumb,Fanart,Siteurl):
        #retourne l'url final
        return '%s?site=%s&function=%s&title=%s&thumb=%s&fanart=%s&%s' % (Pluginurl, Site, Function, Title, Thumb, Fanart, Siteurl)   
        
        
    def endOfDirectory(self):
        xbmcplugin.addSortMethod(Pluginhandle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(Pluginhandle,True,cacheToDisc=True) #cache pas vraiment nécessaire    
  
