#-*- coding: utf-8 -*-
#https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.test.util import VSlog,VSgetsetting,VSlang
from resources.test.gui import cGui

from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.db import cDb
import xbmcgui

SITE_IDENTIFIER = 'cHome'

Deco = '%s [COLOR '+VSgetsetting('deco_color')+'](%s)[/COLOR]'

oGui = cGui()

# >>>> suivre cet ordre >>>> site fonction name thumb fanart 5eme argument

# le 5 eme argument est reservé soit a l'url format("siteUrl=http://venom") soit a oOutputParameterHandler
# oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
# oOutputParameterHandler.addParameter('disp', match[2])
# params = oOutputParameterHandler.getParameterAsUri()

#>>>>>>("globalSearch", "searchMovie", VSlang(30077)+": "+"Films", "search.png", "search_fanart.jpg", params)

#sauf pour HomeSubFolder

class cHome:
    def __init__(self):
        self.Submenu = []

        
    def load(self):

        Menu = []

        if (VSgetsetting('home_cherches') == 'true'):
            Menu.append((SITE_IDENTIFIER , "showSearch", VSlang(30076), "search.png", "search_fanart.jpg", "siteUrl=http://venom"))

        if (VSgetsetting('home_cherchev') == 'true'):
            Menu.append(("themoviedb_org", "load", VSlang(30088), "searchtmdb.png", "vsearch_fanart.jpg", "siteUrl=http://venom"))

        if (VSgetsetting('home_tvs') == 'true'):
            Menu.append(("freebox", "load", VSlang(30115), "tv.png", "tv_fanart.jpg", "siteUrl=http://venom"))

        if (VSgetsetting('home_replaytvs') == 'true'):
            Menu.append((SITE_IDENTIFIER, "showReplay", VSlang(30117), "replay.png", "replay_fanart.jpg", "siteUrl=http://venom"))

        if (VSgetsetting('home_films') == 'true'):
            Menu.append((SITE_IDENTIFIER, "showMovies" , VSlang(30120), "films.png", "films_fanart.jpg", "siteUrl=http://venom"))

        if (VSgetsetting('home_series') == 'true'):
            Menu.append((SITE_IDENTIFIER, "showSeries" , VSlang(30121), "series.png", "series_fanart.jpg", "siteUrl=http://venom"))

        if (VSgetsetting('home_anims') == 'true'):
            Menu.append((SITE_IDENTIFIER, "showAnimes" , VSlang(30122), "animes.png", "animes_fanart.jpg", "siteUrl=http://venom"))

        if (VSgetsetting('home_docs') == 'true'):
            Menu.append((SITE_IDENTIFIER, "showDocs" , VSlang(30112), "doc.png", "doc_fanart.jpg", "siteUrl=http://venom"))

        if (VSgetsetting('home_sports') == 'true'):
            Menu.append(("sitehandler", "callplugin", VSlang(30113), "sport.png", "sport_fanart.jpg", "siteUrl=SPORT_SPORTS"))

        if (VSgetsetting('home_videos') == 'true'):
            Menu.append((SITE_IDENTIFIER, "showNets", VSlang(30114), "buzz.png", "buzz_fanart.jpg", "siteUrl=http://venom"))
            
        #dossiers fixe
        Trakt = ("cTrakt", "getLoad", "Trakt", "trakt.png", "fanart.jpg", "siteUrl=http://venom")
        
        Download = ("cDownload", 'getDownload', VSlang(30202), "download.png", "download_fanart.jpg", "siteUrl=http://venom")
        
        Librairie = ("cLibrary", "getLibrary", VSlang(30300), "library.png", "library_fanart.jpg", "siteUrl=http://venom")
        
        Sources = ("globalSources", "showSources", VSlang(30116), "host.png", "host_fanart.jpg", "siteUrl=http://venom")
        
        Marque = ('cFav', 'getFavourites', VSlang(30210), 'mark.png', "mark_fanart.jpg", "siteUrl=http://venom")

        Menu.extend([Trakt,Download,Librairie,Sources,Marque])

        #maj en dernier
        if (VSgetsetting('home_update') == 'true'):
            Menu.append(("MAJ", "showUpdate", VSlang(30418), "update.png", "update_fanart.jpg", "siteUrl=http://venom"))
  

        oGui.HomeFolder(Menu)
        
        oGui.endOfDirectory()
        
    def showSearch(self):    

        Films_params = "http://venom&disp=search1&type="+VSgetsetting('search1_type')+"&readdb=True"
        
        Films = (VSlang(30077)+": "+VSgetsetting('search1_label'), "search.png", Films_params)
        
        Series_params = "http://venom&disp=search2&type="+VSgetsetting('search2_type')+"&readdb=True"
        
        Series = (VSlang(30089)+": "+VSgetsetting('search2_label'), "search.png", Series_params)
        
        Animes_params = "http://venom&disp=search3&type="+VSgetsetting('search3_type')+"&readdb=True"
        
        Animes = (VSlang(30090)+": "+VSgetsetting('search3_label'), "search.png", Animes_params)
        
        Docs_params = "http://venom&disp=search4&type="+VSgetsetting('search4_type')+"&readdb=True"
        
        Docs = (VSlang(30091)+": "+VSgetsetting('search4_label'), "search.png",  Docs_params)
        
        Choix_params = "http://venom&disp=search5&readdb=True"
        
        Choix = (('%s 5: %s') % (VSlang(30076), VSlang(30092)), "search.png", Choix_params)
        
        Alluc_params = "http://venom&disp=search10&readdb=True"
        
        Alluc = (VSlang(30417), "search.png", "search_fanart.jpg", Alluc_params)
        
        History = ("DoNothing" , "DoNothing", VSlang(30416), "none.png", "search_fanart.jpg", "siteUrl=http://venom")

        self.Submenu.extend([Films,Series,Animes,Docs,Choix,Alluc])
        
        #dossier recherche
        oGui.HomeSubFolder("globalSearch", "searchMovie","search_fanart.jpg",self.Submenu)
 
        if (VSgetsetting("history-view") == 'true'):
            row = cDb().get_history()
            olist = []
            if row:
                #text historique
                oGui.HomeFolder([History])
                for match in row:
                    oOutputParameterHandler = cOutputParameterHandler()

                    #code to get type with disp
                    type = VSgetsetting('search' + match[2][-1:] + '_type')
                    if type:
                        oOutputParameterHandler.addParameter('type', type)
                        xbmcgui.Window(10101).setProperty('search_type', type)

                    oOutputParameterHandler.addParameter('searchtext', match[1])
                    oOutputParameterHandler.addParameter('disp', match[2])
                    oOutputParameterHandler.addParameter('readdb', 'False')
            
                    sParams = oOutputParameterHandler.getParameterAsUri()

                    aEntry = ("globalSearch", "searchMovie", match[1], "search.png", "search_fanart.jpg", sParams)
            
                    olist.append(aEntry)
                    
                #historique
                oGui.HomeFolder(olist,History=True)
                
                #supprimer l'historique
                oGui.HomeFolder([(SITE_IDENTIFIER, 'delSearch', VSlang(30413), "search.png", "search_fanart.jpg" , "siteUrl=http://venom")])

        oGui.endOfDirectory()
        
    # <<<  un site une fonction un fanart - une liste  >>>
    def showReplay(self): 

        Replay_news = ( Deco % (VSlang(30117), VSlang(30101)), "news.png", "REPLAYTV_NEWS")
        
        Replay_genres = ( Deco % (VSlang(30117), VSlang(30105)), "genres.png", "REPLAYTV_GENRES")
        
        Replay_sources = ( VSlang(30138), "host.png", "REPLAYTV_REPLAYTV")
 
        self.Submenu.extend([Replay_news,Replay_genres,Replay_sources])
 
        oGui.HomeSubFolder("sitehandler","callplugin","replay_fanart.jpg",self.Submenu)
        
        oGui.endOfDirectory()

    def showMovies(self):

        Films_news = (Deco % (VSlang(30120), VSlang(30101)), "news.png", "MOVIE_NEWS")
        
        Films_hd = (Deco % (VSlang(30120), VSlang(30160)), "films_hd.png", "MOVIE_HD")
        
        Films_views = (Deco % (VSlang(30120), VSlang(30102)), "views.png",  "MOVIE_VIEWS")
        
        Films_coms = (Deco % (VSlang(30120), VSlang(30103)), "comments.png", "MOVIE_COMMENTS")
        
        Films_notes = (Deco % (VSlang(30120), VSlang(30104)), "notes.png", "MOVIE_NOTES")
        
        Films_genres = (Deco % (VSlang(30120), VSlang(30105)), "genres.png", "MOVIE_GENRES")
        
        Films_years = (Deco % (VSlang(30120), VSlang(30106)), "annees.png",  "MOVIE_ANNEES")
        
        Films_sources = (VSlang(30138), "host.png", "MOVIE_MOVIE")

        self.Submenu.extend([Films_news,Films_hd,Films_views,Films_coms,Films_notes,Films_genres,Films_years,Films_sources])
 
        oGui.HomeSubFolder("sitehandler","callplugin","films_fanart.jpg",self.Submenu)
        
        oGui.endOfDirectory()

    def showSeries(self):
   
        Series_news = (Deco % (VSlang(30121), VSlang(30101)), "news.png", "SERIE_NEWS")
        
        Series_hd = (Deco % (VSlang(30121), VSlang(30160)), "films_hd.png", "SERIE_HD")
        
        Series_genres = (Deco % (VSlang(30121), VSlang(30105)), "genres.png", "SERIE_GENRES")
        
        Series_years = (Deco % (VSlang(30121), VSlang(30106)), "annees.png", "SERIE_ANNEES")
        
        Series_vf = (Deco % (VSlang(30121), VSlang(30107)), "vf.png", "SERIE_VFS")
        
        Series_vostfr = (Deco % (VSlang(30121), VSlang(30108)), "vostfr.png", "SERIE_VOSTFRS")
        
        Series_sources = (VSlang(30138) , "host.png", "SERIE_SERIES")

        self.Submenu.extend([Series_news,Series_hd,Series_genres,Series_years,Series_vf,Series_vostfr,Series_sources])
  
        oGui.HomeSubFolder("sitehandler","callplugin","series_fanart.jpg",self.Submenu)
        
        oGui.endOfDirectory()
 
    def showAnimes(self):
 
        Animes_news = (Deco % (VSlang(30122), VSlang(30101)),"news.png", "ANIM_NEWS")
        
        Animes_vf = (Deco % (VSlang(30122), VSlang(30107)), "vf.png", "ANIM_VFS")
        
        Animes_vostfr = (Deco % (VSlang(30122), VSlang(30108)), "vostfr.png", "ANIM_VOSTFRS")
        
        Animes_genres = (Deco % (VSlang(30122), VSlang(30105)), "genres.png", "ANIM_GENRES")
        
        Animes_years = (Deco % (VSlang(30122), VSlang(30106)), "annees.png", "ANIM_ANNEES")
        
        Animes_kids = (Deco % (VSlang(30122), VSlang(30109)), "animes_enfants.png", "ANIM_ENFANTS")
        
        Animes_sources = (VSlang(30138), "host.png", "ANIM_ANIMS")

        self.Submenu.extend([Animes_news,Animes_vf,Animes_vostfr,Animes_genres,Animes_years,Animes_kids,Animes_sources])

        oGui.HomeSubFolder("sitehandler","callplugin","animes_fanart.jpg",self.Submenu)
        
        oGui.endOfDirectory()

    def showDocs(self):
    
        Docs_news = (Deco % (VSlang(30112), VSlang(30101)), "news.png", "DOC_NEWS" )
        
        Docs_genres = (Deco % (VSlang(30112), VSlang(30105)), "genres.png", "DOC_GENRES" )
        
        Docs_sources = (VSlang(30138), "host.png", "DOC_DOCS")

        self.Submenu.extend([Docs_news,Docs_genres,Docs_sources])
  
        oGui.HomeSubFolder("sitehandler","callplugin","doc_fanart.jpg",self.Submenu)

        oGui.endOfDirectory()
        
    def showNets(self): 

        Videos_news = (Deco % (VSlang(30114), VSlang(30101)), "news.png", "NETS_NEWS")
        
        Videos_genres = (Deco % (VSlang(30114), VSlang(30105)), "genres.png", "NETS_GENRES")
        
        Videos_sources = (VSlang(30138), "host.png", "MOVIE_NETS")
 
        self.Submenu.extend([Videos_news,Videos_genres,Videos_sources])

        oGui.HomeSubFolder("sitehandler","callplugin","buzz_fanart.jpg",self.Submenu)
        
        oGui.endOfDirectory()

        
    def delSearch(self):
        cDb().del_history()
