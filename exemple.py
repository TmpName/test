#pense-bête
>> FolderType3 >> genre annee etc..
site , fonction, thumb, fanart, une liste(Nom,Url)

ex: année
    oGui = cGui()
    liste = []
    for i in reversed(xrange(1936, 2018)):
        liste.append((str(i),URL_MAIN + 'series/annee-' + str(i)))

    oGui.FolderType3(SITE_IDENTIFIER, 'showMovies','annees.png' ,'films_fanart.jpg', liste)
    
    oGui.endOfDirectory()
    

ex:genre
    oGui = cGui()
    liste = [
    ('Action',URL_MAIN + 'action/'),
    ('Animation',URL_MAIN +'animation/'),
    ('Aventure',URL_MAIN + 'aventure/'),
    ('Comédie',URL_MAIN + 'comedie/'),
    ('Crime',URL_MAIN + 'crime/'),
    ('Documentaire',URL_MAIN + 'documentaire/'),
    ('Drame',URL_MAIN + 'drame/'),
    ('Etranger',URL_MAIN + 'etranger/'),
    ('Familial',URL_MAIN + 'familial/'),
    ('Fantastique',URL_MAIN + 'fantastique/'),
    ('Guerre',URL_MAIN + 'guerre/'),
    ('Histoire',URL_MAIN + 'histoire/'),
    ('Horreur',URL_MAIN + 'horreur/'),
    ('Musique',URL_MAIN + 'musique/'),
    ('Mystère',URL_MAIN + 'mystere/'),
    ('Romance',URL_MAIN + 'romance/'),
    ('Science Fiction',URL_MAIN + 'science-fiction/'),
    ('Téléfilm',URL_MAIN + 'telefilm/'),
    ('Thriller',URL_MAIN + 'Thriller/'),
    ('Western',URL_MAIN + 'western/')]


    oGui.FolderType3(SITE_IDENTIFIER, 'showMovies', 'genres.png', 'films_fanart.jpg', liste)
    
    oGui.endOfDirectory()
