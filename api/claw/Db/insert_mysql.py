import mysql.connector
import json
import os

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

    def clean_database(self):
        sql= "DELETE FROM artists"
        self.mycursor.execute(sql)
        self.mydb.commit()
    def close(self):
        self.mydb.close()

def add_song_to_db(list_song):
    conn = connect()
    mycursor = conn.mycursor
    mydb = conn.mydb

    sql_artist = 'INSERT IGNORE INTO artists(id,name,link,thumbnail) VALUES '
    sql_song= 'INSERT IGNORE INTO songs(id,name,duration,source,thumbnail,id_artist) VALUES '

    for song in list_song:
        artist = song['artist']
        song["name"] = song["name"].replace("\"","'")
        sql_artist += f'("{artist["id"]}", "{artist["name"]}", "{artist["link"]}","{artist["thumbnail"]}"),'
        sql_song += f'("{song["id"]}", "{song["name"]}", "{song["duration"]}", "{song["source"]}", "{song["thumbnail"]}", "{artist["id"]}"),'

    sql_artist=sql_artist.rstrip(",")
    sql_song=sql_song.rstrip(",")
    # print(sql_artist)
    mycursor.execute(sql_artist)
    mycursor.execute(sql_song)
    mydb.commit()

    conn.close()



    return True



def get_list_song_from_json(name_json):
    data=[]
    with open(name_json, 'r', encoding='utf-8') as old_json_file:
        
        data = json.load(old_json_file)
        
        
    return data


data = get_list_song_from_json(JSON_SONGS_PATH)
print(len(data))
len_data = len(data)
if(len_data>0):
    for i in range(0,len_data,500):
        add_song_to_db(data[i:i+500])
        print(f'{i} xong')

# conn = connect()
# conn.clean_database()
# conn.close()