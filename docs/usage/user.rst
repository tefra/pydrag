User Webservices
================


Retrieve user
-------------

.. code-block :: python

    >>> from pydrag import User
    >>> me = User.find("Zaratoustre")
    >>> me
    User(playlists=0, playcount=34816, gender='n', name='Zaratoustre', url='https://www.last.fm/user/Zaratoustre', country='Greece', image=[Image(size='small', text='https://lastfm-img2.akamaized.net/i/u/34s/a4503fbd410046dcc63317f0fa19613a.png'), Image(size='medium', text='https://lastfm-img2.akamaized.net/i/u/64s/a4503fbd410046dcc63317f0fa19613a.png'), Image(size='large', text='https://lastfm-img2.akamaized.net/i/u/174s/a4503fbd410046dcc63317f0fa19613a.png'), Image(size='extralarge', text='https://lastfm-img2.akamaized.net/i/u/300x300/a4503fbd410046dcc63317f0fa19613a.png')], age=0, registered=1263647609, real_name='Chris T', recent_track=None)
    >>>
    >>> me.name
    'Zaratoustre'
    >>> me.date_registered
    datetime.datetime(2010, 1, 16, 13, 13, 29)
    >>>


Retrieve friends
----------------

.. code-block :: python

    >>> from pydrag import User
    >>>
    >>> me = User.find("Zaratoustre")
    >>> friends = me.get_friends(recent_tracks=True, limit=10, page=1)
    >>> [(x.name, x.recent_track.name) for x in friends]
    [('meichi', 'Pi'), ('demkod', '(bottle back)'), ('STBKilla', 'Nowhere Fast'), ('keret221', 'Letter Home'), ('Lilfix', 'Namorar pra Quê?'), ('Yoji', 'Empire State of Mind (fea
    t. Alicia Keys)'), ('Kastishka', 'Wipe Your Eyes'), ('comingsoon_', 'I Want It All'), ('Bagheera', 'Welcome Home')]
    >>>


Retrieve Artist Lists
---------------------

.. code-block :: python

    >>> from pydrag import User
    >>> from pydrag.constants import Period
    >>>
    >>> me = User.find("Zaratoustre")
    >>>
    >>> artists = me.get_artists(limit=5)

    >>> [x.name for x in artists]
    ['System of a Down', 'Eminem', 'Red Hot Chili Peppers', 'Serj Tankian', 'FF.C']
    >>>
    >>> artists = me.get_top_artists(period=Period.week, limit=5)
    >>> [x.name for x in artists]
    ['FF.C', 'Άλφα Γάμα', 'Terror X Crew', 'Αρτέμης / Ευθύμης', 'DMX']
    >>>
    >>> artists = me.get_weekly_artist_chart()
    >>> [x.name for x in artists]
    ['FF.C', 'Άλφα Γάμα', 'Terror X Crew', 'Αρτέμης / Ευθύμης', 'DMX', 'Eminem', 'Black Eyed Peas', 'Ζωντανοί Νεκροί', "Goin' Through", 'Wu-Tang Clan', '50 Cent', 'The Beatnuts', 'Xzibit', 'Nathaniel Rateliff', 'Placebo', 'Rage Against the Machine', 'Ελένη Βιτάλη']


Retrieve Album Lists
--------------------

.. code-block :: python

    >>> from pydrag import User
    >>> from pydrag.constants import Period
    >>>
    >>> me = User.find("Zaratoustre")
    >>>
    >>> albums = me.get_top_albums(period=Period.overall)
    >>> [x.name for x in albums]
    ['Nathaniel Rateliff & The Night Sweats', 'Elect the Dead', 'Relapse', 'Toxicity', 'Με Λένε Πόπη', 'Hypnotize', 'Mezmerize', 'Steal This Album!', 'Bestwishes', 'Past Masters', 'The Better Life', 'System of a Down', 'Californication', 'Demon Days', 'A Real Dead One', 'Κλασικα Ηχογραφημενα', 'Hot Fuss', 'The Black Parade', 'Back to Bedlam', 'Recovery', 'Monkey Business', 'The Getaway', 'Danger Days: The True Lives of the Fabulous Killjoys', 'Live in Texas', 'Harakiri', 'Αντιληψίες συνείδησης', "It's Dark And Hell Is Hot", 'Sting In The Tail', 'Blood Sugar Sex Magik', 'American IV: The Man Comes Around', 'Η Απειλή', 'True Blood Volume 1', 'Lovers', 'Sigh No More', 'Imperfect Harmonies', 'Before I Self Destruct', 'The Eminem Show', "Υπ'Οψιν", 'Hengen Jizai no Magical Star', 'Beggars Banquet', 'History Begins', 'The Razors Edge', 'Back in Black', 'The Best Damn Thing', 'Deep Purple in Rock: Anniversary Edition 1995', 'Let It Be', 'With the Lights Out', 'Ο Ρομπέν των χαζών (Rodon Live)', 'Appetite for Destruction', 'Fear of the Dark']
    >>>
    >>> albums = me.get_weekly_album_chart()
    >>> [x.name for x in albums]
    ['Αγνωστοφοβία', 'Κλασικα Ηχογραφημενα', "Υπ'Οψιν", 'Η Απειλή', "Σ'άλλη Διάσταση", 'Αντιληψίες συνείδησης', 'Έσσεται Ήμαρ', 'Οχυρωμένη αντίληψη', 'Η Πόλις Εάλω', 'Monkey Business', 'Εγείρεσθε άγωμεν εντεύθεν', 'ΖΝ Εντολές', 'Νεοέλληνα Άκου', 'Ο διαλεχτός της άρνησης κι ο ακριβογιός της πίστης', 'The Duets', 'The Marshall Mathers LP2', 'The W', 'Year Of The Dog... Again', '8 Mile', 'Before I Self Destruct', "It's Dark And Hell Is Hot", 'Restless', 'TAKE IT OR SQUEEZE IT', 'Σκληροί Καιροί', 'Nathaniel Rateliff & The Night Sweats', 'Rage Against the Machine', 'Sleeping with Ghosts', 'Terror X Crew', 'Η γεύση του μένους', 'Το απέναντι μπαλκόνι']



Retrieve Track Lists
--------------------

.. code-block :: python

    >>> from pydrag import User
    >>> from pydrag.constants import Period
    >>>
    >>> me = User.find("Zaratoustre")
    >>>
    >>> tracks = me.get_artist_tracks(artist="queen", page=2)
    >>> set([x.name for x in tracks])
    {'We Will Rock You', 'The Miracle', 'You and I', 'White Queen (As It Began)', 'Somebody to Love', 'Under Pressure', 'The Show Must Go On', "'39", "You're My Best Friend", 'Spread Your Wings', 'Another One Bites the Dust', 'Killer Queen', 'We Are the Champions', 'Nevermore', 'Fat Bottomed Girls', "Modern Times Rock 'N' Roll", 'Gimme the Prize', 'Bohemian Rhapsody', 'A Kind of Magic', 'Delilah', 'Bicycle Race', "Don't Stop Me Now", 'Misfire', 'Crazy Little Thing Called Love'}
    >>>
    >>> tracks = me.get_recent_tracks(limit=2, page=2)
    >>> set([x.name for x in tracks])
    {'Η Κλίκα της Στάχτης', 'Το Τελευταίο Γράμμα Ενός Αυτόχειρα'}
    >>>
    >>> tracks = me.get_top_tracks(period=Period.month, limit=2, page=2)
    >>> set([x.name for x in tracks])
    {'Beauty and the Beast', 'Kryptonite'}
    >>>
    >>>
    >>> tracks = me.get_weekly_track_chart()
    >>> set([x.name for x in tracks])
    {'Άσε Με Να Σου Πω', 'Όσο και να σκέφτηκα (Remix)', 'Εφιάλτες', "Ruff Ryder's Anthem", 'Δεύτερον', 'X (Feat. Snoop Dogg)', 'Παλιό Ποτό', 'MCs & DJs', 'Κράτα απόσταση (ft. Dash)', 'Χρηματολαγνεία', 'Ο κύκλος', 'Δεν αρκεί', 'Αντίδοτο', 'Παραμύθι (feat Deadlock) Remix', "No Escapin' This", 'Rap God', 'Dibi Dibi Song', 'Μη Φοβάσαι', 'Το Τελευταίο Γράμμα Ενός Αυτόχειρα', 'Ορχηστρικό 2', 'Πάρε Λίγο Φως (Remix)', 'Ω, Ναι', 'Οι Στίχοι Μας Ποτέ Δεν Σταματάνε', 'Έλα Μου', 'Επιτέλους Αρχή', 'Αγνωστοφοβία', 'Το Ημερολόγιο', 'Μακρύς, Βαρύς Χειμώνας', 'Στημένο παιχνίδι', 'Η δικιά μου Ιθάκη', 'Δήλωση', 'Βαρέθηκα', 'Η Αφύπνησις', 'συνοποσία', 'Άλλη Μια Άρχη', 'Το όριο', 'Φταίω Κι Εγώ', 'WE GOT TO PUMP IT UP', 'Ανάθεμα', 'Άλλο Ένα Αντίο', 'Θολά Νερά', 'Έτσι Το Ζω', 'Δέκα Πόντους Τακούνι', 'Άντε Να Δούμε Που Θα Φτάσει', 'Λεπτή γραμμή', 'Η νύχτα των ζωντανών νεκρών', 'Με χρέος μεγάλο', 'Ανήθικο μου στυλ (ft. Χαρμάνης)', 'Είσαι Ακόμα Εδώ', 'Όπως πρώτα (βαρεία μίξις)', 'Επίλογος', 'Ο dj alx στον τεκέ', 'Νεοέλληνα Άκου', 'Αρκετά Για Να Μαθαίνεις', 'Η κιβωτός', 'Προοίμιον', 'Όπως πρώτα (Gauloise mix)', 'Παιχνίδια του μυαλού', 'Απολογισμός', 'Οι στίχοι μας ποτέ δεν σταματάνε (ηλεκτρική καρέκλα)', 'Goodbye', "Don't Phunk with My Heart", 'Πισώπλατα', 'Hold Me Down', "Ριμοθέτηση '98", 'Ωδή εις το γκούτσι φόρεμα', 'Εκδοχή', 'The Bitter End', 'Μια φορά και έναν καιρό', 'Ριπή', 'Όσα μου έμαθες εσύ', 'Ποτέ Δεν Είναι Αργά', 'Περίφημη Τετράδα', 'Παραμύθι', 'Άδειο Σκηνικό', 'Ξύπνιος μέσα στα όνειρα κάποιων άλλων', 'I Need Never Get Old', 'Η Κλίκα της Στάχτης', 'Killing in the Name', 'Μια διαπίστωση', 'Νέος τρόπος σκέψης', 'Pump It', 'Φωτεινός Ορίζοντας', 'Για τα λεφτά γίνονται όλα', 'Περσεφόνη', 'Το ξόδι (σκοταδισμός Β Α)', "Που 'ν' οι Πέννες σας;", 'Ο Έλληνας που έχεις συνηθίσει', 'Funky scratch', 'Δίκασμα', 'Υποθέσεις', 'Ηλιακή φύσις', 'Συζητώντας Με Έμενα', 'Ψυχικά νεκρός', 'Η πιο παλιά μάχη', 'Lose Yourself', 'Outro (ορχηστρικό)', 'Σημεία Των Καιρών', "Συναγερμός (Jungle Mix ''''98)", 'Πανικόβλητον', 'Η πτώση (feat. Ημισκούμπρια, Terror X Crew)', 'Protect Ya Neck (The Jump Off)', 'Δούρειος ήχος', 'Πρίσμα Φαντασίας', 'Κάποιοι', 'Ρυθμοδαμαστής & Πάνας'}
    >>>
    >>> tracks = me.get_loved_tracks(limit=5, page=2)
    >>> set([x.name for x in tracks])
    {'Carry on Wayward Son', 'Το Τελευταίο Γράμμα Ενός Αυτόχειρα', 'Εχω Το Θεμα Μου', 'Πάρε Λίγο Φως (Remix)', 'Strange Love'}
    >>>



Retrieve Tag Lists
------------------

.. code-block :: python

    >>> from pydrag import User
    >>>
    >>> me = User.find("Zaratoustre")
    >>>
    >>> tags = me.get_personal_tags(tag="metal", category="artist")
    >>> [t.name for t in tags]
    >>>
    >>> tags = me.get_personal_tags(tag="metal", category="album")
    >>> [t.name for t in tags]
    >>>
    >>> tags = me.get_personal_tags(tag="metal", category="track")
    >>> [t.name for t in tags]
    >>>
    >>> tags = me.get_top_tags(limit=5)
    >>> [t.name for t in tags]
    ['foo', 'bar', 'super']
