import json
import requests
import tidalapi
import time
from secrets import spotify_token, tidal_login, tidal_password

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_songs():

    tracks = []

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {spotify_token}",
    }

    query = "https://api.spotify.com/v1/me/tracks?limit=10&offset=5"

    while True:
        response = requests.get(
            query,
            headers=headers
        )

        for track in response.json()["items"]:
            tracks.append(track["track"])

        query = response.json()["next"]

        if response.json()["next"] == None:
            break
    return tracks

def add_tidal(spotify_tracks):
    session = tidalapi.Session()
    session.login(tidal_login, tidal_password)
    user = tidalapi.User(session,session.user.id)


    for spotify_track in spotify_tracks:
        found = False
        tidal_results = session.search('track', spotify_track, limit=15)

        print(bcolors.OKBLUE + "SPOTIFY SONG: " + spotify_track + " - " + spotify_tracks[spotify_track])


        if len(tidal_results.tracks) > 0:
            count = 1
            print(bcolors.HEADER + "TIDAL RESULTS:")
            for tidal_track in tidal_results.tracks:
                print(bcolors.HEADER + "    " + str(count) + ". " + tidal_track.name + " - " + tidal_track.artist.name)
                count = count + 1
        else:
            print(bcolors.FAIL + "NOT FOUND \n")
            print(bcolors.HEADER + "---------------------------------------- \n")
            found = True

        for tidal_track in tidal_results.tracks:
            if tidal_track.artist.name == spotify_tracks[spotify_track]:
                print(bcolors.OKGREEN + "ONE MATCH > " + tidal_track.name + " - " + tidal_track.artist.name)
                print(bcolors.HEADER + "---------------------------------------- \n")
                try:
                    time.sleep(10)
                    print(bcolors.HEADER + "ADDING TRACK")
                    user.favorites.add_track(tidal_track.id)
                    print(bcolors.OKGREEN + "DONE")
                except:
                    print(bcolors.FAIL + "FAIL")
                
                found = True
                break

        if not found:
            print(bcolors.FAIL + "NO ONE MATCH \n")
            print(bcolors.HEADER + "---------------------------------------- \n")


def main():
    spotify_tracks_json = get_songs()
    spotify_tracks = {}

    for track in spotify_tracks_json:
        spotify_tracks[track["name"]] = track["artists"][0]["name"]

    add_tidal(spotify_tracks)

if __name__ == "__main__":
    main()