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
  

        oGui.addSimpleFolder(Menu)
        
        oGui.endOfDirectory()
        
    def showSearch(self):    

        
        Films_params = "siteUrl=http://venom&disp=search1&type="+VSgetsetting('search1_type')+"&readdb=True"
        
        Films = ("globalSearch", "searchMovie", VSlang(30077)+": "+VSgetsetting('search1_label'), "search.png", "search_fanart.jpg", Films_params)
        
        Series_params = "siteUrl=http://venom&disp=search2&type="+VSgetsetting('search2_type')+"&readdb=True"
        
        Series = ("globalSearch", "searchMovie", VSlang(30089)+": "+VSgetsetting('search2_label'), "search.png", "search_fanart.jpg", Series_params)
        
        Animes_params = "siteUrl=http://venom&disp=search3&type="+VSgetsetting('search3_type')+"&readdb=True"
        
        Animes = ("globalSearch", "searchMovie", VSlang(30090)+": "+VSgetsetting('search3_label'), "search.png", "search_fanart.jpg", Animes_params)
        
        Docs_params = "siteUrl=http://venom&disp=search4&type="+VSgetsetting('search4_type')+"&readdb=True"
        
        Docs = ("globalSearch", "searchMovie", VSlang(30091)+": "+VSgetsetting('search4_label'), "search.png", "doc_fanart.jpg", Docs_params)
        
        Choix_params = "siteUrl=http://venom&disp=search5&readdb=True"
        
        Choix = ("globalSearch", "searchMovie", ('%s 5: %s') % (VSlang(30076), VSlang(30092)), "search.png", "search_fanart.jpg", Choix_params)
        
        Alluc_params = "siteUrl=http://venom&disp=search10&readdb=True"
        
        Alluc = ("globalSearch", "searchMovie", VSlang(30417), "search.png", "search_fanart.jpg", Alluc_params)
        
        History = ("None" , "DoNothing", VSlang(30416), "search.png", "search_fanart.jpg", "siteUrl=http://venom")

        self.Submenu.extend([Films,Series,Animes,Docs,Choix,Alluc])
        #dossier recherche
        oGui.addSimpleFolder(self.Submenu)
 
        if (VSgetsetting("history-view") == 'true'):
            row = cDb().get_history()
            olist = []
            if row:
                #text historique
                oGui.addSimpleFolder([History])
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
                oGui.addHistoryFolder(olist)
                #supprimer l'historique
                oGui.addSimpleFolder([(SITE_IDENTIFIER, 'delSearch', VSlang(30413), "search.png", "search_fanart.jpg" , "siteUrl=http://venom")])

        oGui.endOfDirectory()
 
    def showReplay(self): 

        Replay_news = ("sitehandler", "callplugin",Deco % (VSlang(30117), VSlang(30101)), "news.png", "replay_fanart.jpg","siteUrl=REPLAYTV_NEWS")
        
        Replay_genres = ("sitehandler","callplugin",Deco % (VSlang(30117), VSlang(30105)), "genres.png", "replay_fanart.jpg", "siteUrl=REPLAYTV_GENRES")
        
        Replay_sources = ("sitehandler", "callplugin", VSlang(30138), "host.png", "replay_fanart.jpg", "siteUrl=REPLAYTV_REPLAYTV")
 
        self.Submenu.extend([Replay_news,Replay_genres,Replay_sources])
 
        oGui.addSimpleFolder(self.Submenu)
        
        oGui.endOfDirectory()

    def showMovies(self):

        Films_news = ("sitehandler", "callplugin", Deco % (VSlang(30120), VSlang(30101)),"news.png", "films_fanart.jpg", "siteUrl=MOVIE_NEWS")
        
        Films_hd = ("sitehandler", "callplugin", Deco % (VSlang(30120), VSlang(30160)), "films_hd.png", "films_fanart.jpg", "siteUrl=MOVIE_HD")
        
        Films_views = ("sitehandler", "callplugin",Deco % (VSlang(30120), VSlang(30102)), "views.png", "films_fanart.jpg", "siteUrl=MOVIE_VIEWS")
        
        Films_coms = ("sitehandler", "callplugin", Deco % (VSlang(30120), VSlang(30103)), "comments.png", "films_fanart.jpg", "siteUrl=MOVIE_COMMENTS")
        
        Films_notes = ("sitehandler", "callplugin", Deco % (VSlang(30120), VSlang(30104)), "notes.png", "films_fanart.jpg", "siteUrl=MOVIE_NOTES")
        
        Films_genres = ("sitehandler", "callplugin", Deco % (VSlang(30120), VSlang(30105)), "genres.png", "films_fanart.jpg", "siteUrl=MOVIE_GENRES")
        
        Films_years = ("sitehandler", "callplugin",  Deco % (VSlang(30120), VSlang(30106)), "annees.png", "films_fanart.jpg", "siteUrl=MOVIE_ANNEES")
        
        Films_sources = ("sitehandler", "callplugin", VSlang(30138), "host.png", "films_fanart.jpg", "siteUrl=MOVIE_MOVIE")

        self.Submenu.extend([Films_news,Films_hd,Films_views,Films_coms,Films_notes,Films_genres,Films_years,Films_sources])
 
        oGui.addSimpleFolder(self.Submenu)
        
        oGui.endOfDirectory()

    def showSeries(self):
   
        Series_news = ("sitehandler", "callplugin", Deco % (VSlang(30121), VSlang(30101)), "news.png", "series_fanart.jpg", "siteUrl=SERIE_NEWS")
        
        Series_hd = ("sitehandler", "callplugin", Deco % (VSlang(30121), VSlang(30160)), "films_hd.png", "series_fanart.jpg", "siteUrl=SERIE_HD")
        
        Series_genres = ("sitehandler","callplugin", Deco % (VSlang(30121), VSlang(30105)), "genres.png", "series_fanart.jpg", "siteUrl=SERIE_GENRES")
        
        Series_years = ("sitehandler","callplugin", Deco % (VSlang(30121), VSlang(30106)), "annees.png", "series_fanart.jpg", "siteUrl=SERIE_ANNEES")
        
        Series_vf = ("sitehandler", "callplugin", Deco % (VSlang(30121), VSlang(30107)), "vf.png", "series_fanart.jpg", "siteUrl=SERIE_VFS")
        
        Series_vostfr = ("sitehandler", "callplugin", Deco % (VSlang(30121), VSlang(30108)), "vostfr.png", "series_fanart.jpg", "siteUrl=SERIE_VOSTFRS")
        
        Series_sources = ("sitehandler", "callplugin", VSlang(30138) , "host.png", "series_fanart.jpg", "siteUrl=SERIE_SERIES")

        self.Submenu.extend([Series_news,Series_hd,Series_genres,Series_years,Series_vf,Series_vostfr,Series_sources])
  
        oGui.addSimpleFolder(self.Submenu)
        
        oGui.endOfDirectory()
 
    def showAnimes(self):
 
        Animes_news = ("sitehandler", "callplugin", Deco % (VSlang(30122), VSlang(30101)),"news.png","animes_fanart.jpg", "siteUrl=ANIM_NEWS")
        
        Animes_vf = ("sitehandler", "callplugin", Deco % (VSlang(30122), VSlang(30107)), "vf.png", "animes_fanart.jpg", "siteUrl=ANIM_VFS")
        
        Animes_vostfr = ("sitehandler","callplugin", Deco % (VSlang(30122), VSlang(30108)), "vostfr.png", "animes_fanart.jpg", "siteUrl=ANIM_VOSTFRS")
        
        Animes_genres = ("sitehandler", "callplugin", Deco % (VSlang(30122), VSlang(30105)), "genres.png", "animes_fanart.jpg", "siteUrl=ANIM_GENRES")
        
        Animes_years = ("sitehandler","callplugin", Deco % (VSlang(30122), VSlang(30106)), "annees.png", "animes_fanart.jpg", "siteUrl=ANIM_ANNEES")
        
        Animes_kids = ("sitehandler", "callplugin", Deco % (VSlang(30122), VSlang(30109)), "animes_enfants.png", "animes_fanart.jpg", "siteUrl=ANIM_ENFANTS")
        
        Animes_sources = ("sitehandler", "callplugin", VSlang(30138), "host.png", "animes_fanart.jpg", "siteUrl=ANIM_ANIMS")

        self.Submenu.extend([Animes_news,Animes_vf,Animes_vostfr,Animes_genres,Animes_years,Animes_kids,Animes_sources])

        oGui.addSimpleFolder(self.Submenu)
        
        oGui.endOfDirectory()

    def showDocs(self):
    
        Docs_news = ("sitehandler", "callplugin", Deco % (VSlang(30112), VSlang(30101)), "news.png", "doc_fanart.jpg", "siteUrl=DOC_NEWS" )
        
        Docs_genres = ("sitehandler", "callplugin", Deco % (VSlang(30112), VSlang(30105)), "genres.png", "doc_fanart.jpg", "siteUrl=DOC_GENRES" )
        
        Docs_sources = ("sitehandler", "callplugin", VSlang(30138), "host.png", "doc_fanart.jpg", "siteUrl=DOC_DOCS")

        self.Submenu.extend([Docs_news,Docs_genres,Docs_sources])
  
        oGui.addSimpleFolder(self.Submenu) 
        
        oGui.endOfDirectory()
        
    def showNets(self): 

        Videos_news = ("sitehandler", "callplugin", Deco % (VSlang(30114), VSlang(30101)), "news.png", "vstreamfanart.jpg", "siteUrl=NETS_NEWS")
        
        Videos_genres = ("sitehandler", "callplugin", Deco % (VSlang(30114), VSlang(30105)), "genres.png", "vstreamfanart.jpg", "siteUrl=NETS_GENRES")
        
        Videos_sources = ("sitehandler", "callplugin", VSlang(30138), "host.png", "vstreamfanart.jpg", "siteUrl=MOVIE_NETS")
 
        self.Submenu.extend([Videos_news,Videos_genres,Videos_sources])

        oGui.addSimpleFolder(self.Submenu)
        
        oGui.endOfDirectory()

        
    def delSearch(self):
        cDb().del_history()
