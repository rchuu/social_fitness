import spotipy
from spotipy import SpotifyClientCredentials

cid = '0a4c36fea33d439cb53856de91e923e5'
secret = '2710be3ea1474a858c9ca6fa59c41fa7'
auth_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)
# to create a spotify documentation
sp = spotipy.Spotify(auth_manager=auth_manager)
results = sp.search("Beyonce")  # to create an client object
print(results)
