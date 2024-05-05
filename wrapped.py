import os
import requests
import base64
import spotipy
import serpapi
from PIL import Image
from io import BytesIO

def main():
  while True:
    my_username=input("Please input your Spotify username: ").strip()
    if my_username!='':
      break
    else:
      print("Please enter a username")

  try:
    token=spotipy.util.prompt_for_user_token(my_username,scope=['playlist-modify-public','user-library-read',"playlist-read-private",
                                                                'ugc-image-upload','playlist-modify-private'],
                                             client_id= os.environ['SPOTIPY_CLIENT_ID'], client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
                                             redirect_uri= os.environ['SPOTIPY_REDIRECT_URI'])  #try to import these secrets
  except:
    os.remove(f".cache-{my_username}")



  spotify=spotipy.Spotify(auth=token)


  user=spotify.current_user()

  while True:
    name=input("Write the name of the artist you wish to make your own personalized playlist of: ").strip().lower()
    if name!='':
      break
    else:
      print("Please enter a name for an artist")

  while True:
    yes_or_no=input("When you add a song to your playlist, do you also add it to \"My Liked Songs\"? (yes/no): ").strip().lower()
    if yes_or_no == "yes" or yes_or_no=="no":
      break
    else:
      print("Please input yes/no")

  if yes_or_no=="yes":
    artist_id, artist_name=get_artist_id(spotify,name)

    artist_songs=get_artist_songs_to_add(spotify, artist_id)

    #check to see if the user has each song saved
    playlist=create_playlist(spotify, artist_songs,artist_name,user)
  else:
    _,artist_name=get_artist_id(spotify,name)
    user_songs=get_songs_to_add(spotify, artist_name, my_username)
  
    playlist=create_playlist(spotify, user_songs,artist_name,user) 

  change_playlist_cover(spotify, playlist, artist_name) 

  



def get_artist_id(spotify,name=''):
  artist=(spotify.search(name, type="artist"))
  name=artist["artists"]["items"][0]["name"]
  id=artist["artists"]["items"][0]["id"]
  return id, name
  

def get_artist_songs_to_add(spotify, artist_id):
  artist_songs=[]

  for album in spotify.artist_albums(artist_id, album_type="album",limit=50)["items"]:
    album_id=album["id"]
    for song in spotify.album_tracks(album_id)["items"]:
      #have to put song id into a list so the function works
      if spotify.current_user_saved_tracks_contains([song["id"]])==[True] and song["name"] not in artist_songs:
        song_dict={"id":song["id"],"name":song["name"]}

        artist_songs.append(song_dict)
  return artist_songs

  #the albums are under items->albums

def get_songs_to_add(spotify, name, username):
  user_id_songs=[]
  user_combo_songs=[]
  artist_name=""
  for playlist in spotify.current_user_playlists()["items"]:
    if playlist["owner"]["id"]==username:
      playlist_id=playlist["id"]
      total=spotify.playlist_items(playlist_id)["total"]
      i=0
      while(total-i>0):
        for song in spotify.playlist_items(playlist_id, offset=i)["items"]:
          if type(song)!='NoneType':
            for artist in song["track"]["artists"]:
              if artist["name"]==name:
                artist_name=artist["name"]
              else:
                artist_name=song["track"]["artists"][0]["name"]
            
            artist_name_song_name_combo=song["track"]["name"]+name

            if (artist_name_song_name_combo not in user_combo_songs) and artist_name==name:
              user_id_songs.append({"id":song["track"]["id"]})
              user_combo_songs.append(artist_name_song_name_combo)
        i+=100
  return user_id_songs


def create_playlist(spotify, songs_to_add, name, user):
  
  playlist=spotify.user_playlist_create(user["id"], f"Your {name} Playlist", description=f"Your Personalized {name} playlist!")

  for item in songs_to_add:
    spotify.user_playlist_add_tracks(user["id"],playlist["id"], tracks=[item["id"]])
  return playlist


def change_playlist_cover(spotify, playlist, name):
  try:
    search= serpapi.search(engine="google", q=name, tbm="isch", api_key= os.environ["SERPAPI_API_KEY"])
    images = search.as_dict()      
    img_path= images["images_results"][0]["original"]   #get the file path to the artist image
    
    img_request=requests.get(img_path)
    img_data=img_request.content
    max_width = 300
    max_height = 300
    img = Image.open(BytesIO(img_data))
    img.thumbnail((max_width, max_height))

  # Encode the resized image data in base64
    img_buffer = BytesIO()
    img.save(img_buffer, format="JPEG")  # Change the format if the image is not in JPEG format
    artist_img = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
    spotify.playlist_upload_cover_image(playlist["id"], artist_img)
  except:
    print("Unable to change the cover image")
  


if __name__=="__main__":
  main()

