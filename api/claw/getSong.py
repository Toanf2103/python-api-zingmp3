import requests

from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
current_directory = os.path.dirname(__file__)

JSON_ARTISTS_WRITED = os.path.join(current_directory, 'Json/artists_writed.json')
JSON_ARTISTS = os.path.join(current_directory, 'Json/artists.json')

JSON_SONGS = os.path.join(current_directory, 'Json/songs.json')
JSON_SONGS_ID = os.path.join(current_directory, 'Json/songs_id.json')
JSON_SONGS_ERROR = os.path.join(current_directory, 'Json/songs_error.json')




dict_url ={
    "top_song":"http://mp3.zing.vn/xhr/chart-realtime?songId=0&videoId=0&albumId=0&chart=song&time=-1",
    "key_song": lambda id: f"https://mp3.zing.vn/bai-hat/{id}.html",
    "source": lambda key: f"https://mp3.zing.vn/xhr/media/get-source?type=audio&key={key}",
    "artist": lambda artist,page: f"https://mp3.zing.vn{artist}/bai-hat?page={page}",
    "allArtist": "https://mp3.zing.vn/the-loai-nghe-si/Viet-Nam/IWZ9Z08I.html",
    "apiFollow": "https://mp3.zing.vn/xhr/get-follow?ids="
}
def get_top_song():
    response = requests.get(dict_url["top_song"])
    if response.status_code == 200:
        data = response.json()
        return data_return(data['data']['song'])
def get_song_by_id(id):
    
    response = requests.get(dict_url["key_song"](id))
    if response.status_code == 200:
        # Sử dụng BeautifulSoup để phân tích nội dung trang web
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tìm thẻ audio
        
        audio_tag =  soup.find(attrs={'data-xml': True})
        
        # Kiểm tra nếu tìm thấy thẻ audio
        if audio_tag:
            try:
                audio_tag = audio_tag['data-xml'].split('&key=')[-1]
            except:
                audio_tag = audio_tag['data-xml'].split(';key=')[-1]

            url_song = dict_url["source"](audio_tag)
            response = requests.get(url_song)
            if response.status_code == 200:
                data = response.json()
            return data['data']
    return None

def get_all_artist():
    list_artist = []
    end_page = 1
    url = dict_url["allArtist"]
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        end_page=get_end_page(soup)
        # for i in range(1,2):
        for i in range(1,end_page+1):
            list_artist.extend(get_url_artist(i))
    return  list_artist

def get_url_artist(page):
    list_url_artist = []
    url = dict_url["allArtist"]+f"?&page={page}"
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        item_elm = soup.find_all('div',class_="item")
        
        list_folow = []
        for x in item_elm:
            folow = x.find('s',class_="fn-followed")
            list_folow.append(folow['data-id'])
            list_url_artist.append(x.find('a',class_="thumb")["href"])
        
        # call api folow
        url_api_folow = dict_url['apiFollow']+','.join(list_folow)
        response = requests.get(url_api_folow)
        if response.status_code == 200:
            data_folow = response.json()['data']
            list_cook = []
            for i in range(len(list_folow)):
                if data_folow[list_folow[i]] < 7000:
                    list_cook.append(i)
            
            list_url_artist = [list_url_artist[i] for i in range(len(list_url_artist)) if i not in list_cook]
            
    return list_url_artist

def get_all_song_artist(artist):
    songs = []
    end_page=1
    response = requests.get(dict_url["artist"](artist,end_page))
    if response.status_code == 200:
        # Sử dụng BeautifulSoup để phân tích nội dung trang web
        soup = BeautifulSoup(response.text, 'html.parser')
        end_page=get_end_page(soup)
        end_page = end_page if end_page<3 else 2 
    # for i in range(1,2):
    for i in range(1,end_page+1):
        url_page = dict_url["artist"](artist,i)
        response = requests.get(url_page)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            div_element = soup.find('div', class_='list-item full-width')
            if div_element:
                songs.extend(get_song_on_page(div_element)) 
    return data_return(songs)

def get_song_on_page(soup):
    list_song = []
    list_li_song = soup.find_all('li',class_='group fn-song')
    
    for li_song in list_li_song:
        
        id_song = li_song['id'][4:]
        new_song = get_song_by_id(id_song)
        if new_song:
            list_song.append(get_song_by_id(id_song))
        
        
    return list_song

def get_end_page(soup):
    pagination =  soup.select('div.pagination')
   
    if len(pagination) == 0:
        return 1
    li_elements = pagination[0].find_all('li')
    if(len(li_elements)<1):
        return 1
    else:
        li_elements = li_elements[-1]
        end_page = li_elements.select('a')[0]['href'].split('&page=')[-1]
        return int(end_page)

def get_all_song():
    list_song = []
    list_artist = get_all_artist()
    i=1
    for artist in list_artist:
        if i>3:
            break
        
        list_song.extend(get_all_song_artist(artist))
        i+=1
    return list_song


def data_return(list_songs,list_id=[]):
    new_data = []
    list_id=[]
    for song in list_songs:
        new_song={}   
        id=song['id']
        if id in list_id:
            continue
        list_id.append(id)
        try:
            song_data = get_song_by_id(id)
            new_song['id'] = song_data['id']
            new_song['name'] = song_data['name']
            new_song['duration'] = song_data['duration']
            new_song['source'] = song_data['source']['128']
            new_song['thumbnail'] = song_data['thumbnail']
            new_song['artist']={
                'id':song_data['artist']['id'],
                'name':song_data['artist']['name'],
                'link':dict_url["artist"](song_data['artist']['link'],1),
                'thumbnail':song_data['artist']['thumbnail']
            }
            new_data.append(new_song)
            print(f"  {new_song['name']}")
        except:
            write_data_to_json(id,JSON_SONGS_ERROR)
            continue
    return new_data

def write_data_to_json(data,output_file,print_data=False):
    if not isinstance(data,list):
        data = [data]
    with open(output_file, 'r') as old_json_file:
        try:
            old_data = json.load(old_json_file)
        except:
            old_data=[]

    data.extend(old_data)

    with open(output_file, 'w') as combined_json_file:
        json.dump(data, combined_json_file)

    
    



def write_artist_to_json():
    list_artist = get_all_artist()
    write_data_to_json(list_artist, JSON_ARTISTS)

def get_list_id_writed():
    try:
        with open(JSON_SONGS_ID, 'r') as json_file:
            list_song_id_writed = json.load(json_file)
        return list_song_id_writed
    except:
        return []

def get_list_artist_writed():
    try:
        with open(JSON_ARTISTS_WRITED, 'r') as json_file:
            list_artist_writed = json.load(json_file)
        return list_artist_writed
    except json.decoder.JSONDecodeError:
        # Xử lý trường hợp tệp JSON rỗng ở đây
        return []

def write_song_to_json():
    new_data = []
    # Lấy các artist đã load
    list_artist_writed = get_list_artist_writed()

    

    # Lấy tất cả artist 
    with open(JSON_ARTISTS, 'r') as json_file:
        list_artist = json.load(json_file)
    #Lấy những artist chưa load
    list_artist = [artist for artist in list_artist if artist not in list_artist_writed]
    dem=0
    
    for artist in list_artist:
        
        # Lấy các id_song đã load
        list_song_id_writed = get_list_id_writed()

        new_data = get_all_song_artist(artist)
        print(dem,artist,len(new_data))
        new_data_wrire = []
        new_data_id_wrire = []

        for x in new_data:
            if x['id'] not in list_song_id_writed:
                new_data_wrire.append(x)
                
                new_data_id_wrire.append(x['id'])
            
        write_data_to_json(new_data_wrire,JSON_SONGS)
        write_data_to_json(new_data_id_wrire,JSON_SONGS_ID)
        write_data_to_json([artist],JSON_ARTISTS_WRITED)
        dem+=1
        


now = datetime.now()
write_song_to_json()










