import mysql.connector
import json
import os
import re
from unidecode import unidecode

current_directory = os.path.dirname(__file__)
print(current_directory)
dir_folder = os.path.dirname(current_directory)
JSON_SONGS_PATH = os.path.join(dir_folder,"Json\songs.json")



class connect():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="song_mp3"
        )
        self.mycursor = self.mydb.cursor()

    def clean_database(self,table):
        sql= f"DELETE FROM {table}"
        self.mycursor.execute(sql)
        self.mydb.commit()
    def close(self):
        self.mydb.close()

def add_song_to_db(list_song):
    conn = connect()
    mycursor = conn.mycursor
    mydb = conn.mydb

    sql_artist = 'INSERT IGNORE INTO users(id,name,username,password,is_celeb,slug,avatar) VALUES '
    sql_song= 'INSERT IGNORE INTO songs(id,id_user,duration,source,thumbnail,slug) VALUES '

    for song in list_song:
        artist = song['artist']
        slug_song = create_slug(song['name']) + "_" + create_slug(artist['name'])
        slug_artist = create_slug(artist['name'])
        song["name"] = song["name"].replace("\"","'")
        sql_artist += f'("{artist["id"]}", "{artist["name"]}", "{artist["id"]}", "1", 1, "{slug_artist}" , "{artist["thumbnail"]}"),'
        sql_song += f'( "{song["id"]}", "{artist["id"]}", "{song["duration"]}", "{song["source"]}", "{song["thumbnail"]}", "{slug_song}" ),'

    sql_artist=sql_artist.rstrip(",")
    sql_song=sql_song.rstrip(",")
    # print(sql_artist)
    mycursor.execute(sql_artist)
    mycursor.execute(sql_song)
    mydb.commit()

    conn.close()



    return True

def create_slug(name, separator='-'):
    name = unidecode(name)
    # Convert to lowercase
    name = name.lower()

    # Replace spaces with the specified separator
    name = name.replace(' ', separator)

    # Remove non-alphanumeric characters (except for the separator)
    name = re.sub(r'[^a-z0-9' + re.escape(separator) + ']', '', name)

    # Remove leading and trailing separators
    name = name.strip(separator)

    # Remove consecutive separators
    name = re.sub(r'[' + re.escape(separator) + ']+', separator, name)

    return name









def get_list_song_from_json(name_json):
    data=[]
    with open(name_json, 'r', encoding='utf-8') as old_json_file:
        
        data = json.load(old_json_file)
        
        
    return data


data = get_list_song_from_json(JSON_SONGS_PATH)

# if(len_data>0):
#     for i in range(0,len_data,500):
#         add_song_to_db(data[i:i+500])
#         print(f'{i} xong')

# conn = connect()
# conn.clean_database("songs")
# conn.close()

