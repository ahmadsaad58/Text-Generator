
import requests
from bs4 import BeautifulSoup
import os
import re
from argparse import ArgumentParser

# get token
from Token import  GENIUS_API_TOKEN

# Get artist object from Genius API
def request_artist_info(artist_name, page):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response


# Get Genius.com song url's from artist object
def request_song_url(artist_name, song_cap):
    page = 1
    songs = []

    while True:
        response = request_artist_info(artist_name, page)
        json = response.json()
        # Collect up to song_cap song objects from artist
        song_info = []
        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_info.append(hit)

        # Collect song URL's from song objects
        for song in song_info:
            if (len(songs) < song_cap):
                url = song['result']['url']
                songs.append(url)

        if (len(songs) == song_cap):
            break
        else:
            page += 1

    # print('Found {} songs by {}'.format(len(songs), artist_name))
    return songs

# Scrape lyrics from a Genius.com song URL
def scrape_song_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    # remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\[].*?[\]]', '', lyrics)
    # remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    return lyrics


if __name__ == "__main__":
    # create parser
    parser = ArgumentParser(description='Get Songs from Artist')
    parser.add_argument('--fn', '--file', type=str, default='try.txt')
    args = parser.parse_args()

    # open file 
    write_out = open(args.fn, 'a+')
    
    print('**** Enter Quit to Exit ****')
    while (current := input('Enter Artist Name: ')) != 'quit':
        song_num = input('Enter Nummber of Songs you want to pull: ')
        song_urls = request_song_url(current, int(song_num))
        for song in song_urls:
            string = scrape_song_lyrics(song)
            for line in string.split('\n'):
                write_out.write(line)
                write_out.write('\n')
        
    write_out.close()

