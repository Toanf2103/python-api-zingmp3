import mysql.connector
import json
import os
import re
from unidecode import unidecode
from collections import Counter

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
        
        slug_song = song['slug']
       
        

       
        slug_artist = artist['slug']
       

    

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

def check_slug(slug,arr):
    rs = arr.count(slug)
    
    if rs==1:
        return slug
    else:
        kq = slug + "-" + str(rs)
        print(rs,kq)
        return kq

def check_slug_artists(slug,id_artists,arr):
    for x in arr:
        if id_artists == x['id']:
            return x['slug']
    


def set_slug(data):
    
    
    list_slugs_song = []

    for x in data:
        artist = x['artist']
        slug_song = create_slug(x['name']) + "_" + artist['slug']
        list_slugs_song.append(slug_song)
        slug_song =check_slug(slug_song,list_slugs_song)
        x['slug'] = slug_song

        
    return data

        



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



def check_duplicate(table):
    conn = connect()
    mycursor = conn.mycursor
    mydb = conn.mydb
    select_query = f"SELECT slug, COUNT(*) as count FROM {table} GROUP BY slug HAVING count > 1"
    mycursor.execute(select_query)

    # Lấy kết quả truy vấn
    duplicate_slugs = mycursor.fetchall()
    print(duplicate_slugs)
    conn.close()


def find_duplicates(arr):
    count = Counter(arr)
    duplicates = [item for item, freq in count.items() if freq > 1]
    return duplicates

def edit_slug_duplicate(table):
    conn = connect()
    mycursor = conn.mycursor
    mydb = conn.mydb
    
    select_query = f"SELECT id,slug, COUNT(*) as count FROM {table} GROUP BY slug HAVING count > 1"

    mycursor.execute(select_query)

    # Lấy kết quả truy vấn
    duplicate_slugs = mycursor.fetchall()

    # Duyệt qua danh sách slug bị trùng nhau và cập nhật chúng
    
    for slug in duplicate_slugs:
        print(slug)
        for i in range(1, slug[-1]):
            new_slug = f"{slug[1]}-{i+1}"
            update_query = f"UPDATE {table} SET slug = '{new_slug}' WHERE id = '{slug[0]}'"

            # print(update_query)
            # mycursor.execute(update_query)
            # mydb.commit()

    # Lưu các thay đổi vào cơ sở dữ liệu
    

    # Đóng kết nối
    mydb.close()

# edit_slug_duplicate("users")
check_duplicate('songs')

# conn = connect()
# conn.clean_database("users")


# data = get_list_song_from_json(JSON_SONGS_PATH)

# for x in data:
#     url='https://mp3.zing.vn/nghe-si/'
#     artists = x['artist']
#     artists['slug'] = artists['link'].replace(url,'').split('/bai-hat')[0]


# data = set_slug(data)
# len_data = len(data)
# if(len_data>0):
#     for i in range(0,len_data,500):
#         add_song_to_db(data[i:i+500])
#         print(f'{i} xong')

