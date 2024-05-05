from wrapped import get_artist_id, get_artist_songs_to_add, create_playlist,get_songs_to_add,change_playlist_cover, spotipy
spotify=spotipy.Spotify(auth='')


from pytest import raises


def test_get_artist_id():
    with raises (spotipy.exceptions.SpotifyException):
        get_artist_id(spotify,"SZA")
        get_artist_id(spotify,"Jelly Roll")
        get_artist_id(spotify)
def test_get_artist_songs_to_add():
    with raises(spotipy.exceptions.SpotifyException):
        get_artist_songs_to_add(spotify,"5K4W6rqBFWDnAN6FQUkS6x")
        get_artist_songs_to_add(spotify,"INVALID_ID")
        get_artist_songs_to_add("Wrong type","40ZNYROS4zLfyyBSs2PGe2")
def test_create_playlist():
    with raises(TypeError):
        create_playlist(spotify,[{"id":"2eQMC9nJE3f3hCNKlYYHL1", "name": "California Girls"},
                                 {"id":"0r2BUyPTmpbfuz4rR39mLl","name":"I Kissed A Girl"}],"Katy Perry","user") # playlist=create_playlist(spotify, artist_songs,artist_name,user);  playlist=create_playlist(spotify, user_songs,artist_name,user)
        create_playlist(spotify,[{"id":"3pLdWdkj83EYfDN6H2N8MR"},{"id":"7ycBtnsMtyVbbwTfJwRjSP"}, "Kendrick Lamar","user"])
        create_playlist(spotify,"WRONG TYPE","Taylor Swift","user")

def test_get_songs_to_add():
    with raises(spotipy.exceptions.SpotifyException):
        get_songs_to_add(spotify, "Zach Bryan")
        get_songs_to_add(spotify, "Olivia Rodrigo")
        get_songs_to_add(spotify, "Drake")
def test_change_playlist_cover():
        assert change_playlist_cover(spotify, "0bmiseGBmxXIMbFkqw1cqA", "Taylor Swift")==None
        assert change_playlist_cover(spotify, "56uNOccVA2Tv4IrdVCZ1lt", "21 Savage")==None
        assert change_playlist_cover(spotify,"6mjd0ucdddhrzV0qbqXyfd", "Camila Cabello")==None
    


