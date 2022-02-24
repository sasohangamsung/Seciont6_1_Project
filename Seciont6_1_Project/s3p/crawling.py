import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import psycopg2
from pymongo import MongoClient
import pickle

#사이트 받아오기 함수화
def get_page(page_url):

    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup, page

profile_name = ['main_photo', 'name', 'team', 'sex', 'kinds', 'code', 'position', 'birthday', 'weight', 'height', 'school', 'draft']
main_photo_list = []
name_list = []
team_list = []
sex_list = []
kinds_list = []
code_list = []
position_list = []
birth_list = []
weight_list = []
height_list = []
school_list = []
draft_list = []

main_photo = None
p_num = None
p_name = None
p_position = None
p_birth = None
p_weight = None
p_height = None
p_school = None
p_draft = None


col_name = ['이름', '경기구분', '시즌구분', '팀구분', '경기_수', '세트_수', '득점', '공격종합_성공률', '블로킹Avg_set', '서브Avg_set', '세트Avg_set', '리시브효율', '디그Avg_set', '벌칙', '범실']
col0 = []
col1 = []
col2 = []
col3 = []
col4 = []
col5 = []
col6 = []
col7 = []
col8 = []
col9 = []
col10 = []
col11 = []
col12 = []
col13 = []
col14 = []

attack_col_name = ['이름', '공격_시도','공격_성공','범실','상대_블럭','성공률','점유율','성공률1','점유율1']
attack_col0 = []
attack_col1 = []
attack_col2 = []
attack_col3 = []
attack_col4 = []
attack_col5 = []
attack_col6 = []
attack_col7 = []
attack_col8 = []

block_col_name = ['이름','블로킹_시도','블로킹_성공','유효_블로킹','범실','실패','세트당_개수','점유율','성공률','점유율1']
block_col0 = []
block_col1 = []
block_col2 = []
block_col3 = []
block_col4 = []
block_col5 = []
block_col6 = []
block_col7 = []
block_col8 = []
block_col9 = []

sub_col_name = ['이름','서브_시도','서브_성공','범실','세트당_개수','점유율','성공률','점유율1']
sub_col0 = []
sub_col1 = []
sub_col2 = []
sub_col3 = []
sub_col4 = []
sub_col5 = []
sub_col6 = []
sub_col7 = []

set_col_name = ['이름','세트_시도','세트_성공','범실','세트당_개수','점유율','성공률','점유율1']
set_col0 = []
set_col1 = []
set_col2 = []
set_col3 = []
set_col4 = []
set_col5 = []
set_col6 = []
set_col7 = []

recieve_col_name = ['이름','리시브_시도','리시브_정확','리시브_실패','리시브_효율','점유율','성공률','점유율1']
recieve_col0 = []
recieve_col1 = []
recieve_col2 = []
recieve_col3 = []
recieve_col4 = []
recieve_col5 = []
recieve_col6 = []
recieve_col7 = []

dig_col_name = ['이름','디그_시도','디그_정확','디그_실패','세트당_개수','점유율','성공률','점유율1']
dig_col0 = []
dig_col1 = []
dig_col2 = []
dig_col3 = []
dig_col4 = []
dig_col5 = []
dig_col6 = []
dig_col7 = []

rank_text = {}

photo_list = {}





def get_player_list() :

    # 남 : 1 여 : 2
    s_part = list(range(1, 3))
    # 초성 매치 ㄱ:1 ㄴ:2 .... ㅎ:14
    c_type = list(range(1, 15))
    # 선수종류 : 현역 : 1, 기타 : 2, 은퇴 : 3, 외국인 : 4
    p_type = list(range(1, 5))

    for s_ in tqdm(s_part) :
        for c_ in c_type :
            for p_ in p_type :

                soup, page = get_page(f'https://m.kovo.co.kr/team/22000_player_search.asp?s_part={s_}&c_type={c_}&p_type={p_}&t_code=&keyword=')

                if soup.find("ul", class_="r20 wbg mt20") != None :
                    for texts in soup.find("ul", class_="r20 wbg mt20").find_all('a') :

                        texts = texts.text.split("[")
                        name = texts[0][:-1]
                        team = texts[1][0:-1]

                        name_list.append(name)
                        team_list.append(team)

                        sex_list.append(s_)
                        kinds_list.append(p_)

                    codes = [x['href'] for x in soup.find("ul", class_="r20 wbg mt20").find_all('a')]
                    for code in codes :
                        code_list.append(code)



def get_data() :

    for code in tqdm(code_list) :
        player_info_url = f'https://m.kovo.co.kr/team/{code}'

        soup, page = get_page(player_info_url)


        p_num = soup.find('div', class_="playerviw wbg r20").find('p', class_="name").text.split(" ")[0].split(".")[1]
        p_name = ''.join(soup.find('div', class_="playerviw wbg r20").find('p', class_="name").text.split("(")[0].split(" ")[1:])

        main_photo = soup.find('div', class_='thumbs').find('img')['src']
        if main_photo == 'https://www.kovo.co.kr/upfiles/player/' :
            main_photo_list.append('None')
        else :
            main_photo_list.append(main_photo)

        p_position = soup.find('div', class_="playerviw wbg r20").find('p', class_="name").text.split(" ")[-1].split("(")[1][0:-1]
        position_list.append(p_position)

        p_birth = soup.find('div', class_="playerviw wbg r20").find('dl').text.split("\n")[2]
        if p_birth != "년 월 일" and p_birth != "19__년 __월 __일" :
            birth_list.append(p_birth)
        else :
            birth_list.append("None")
        p_height = soup.find('div', class_="playerviw wbg r20").find('dl').text.split("\n")[4].split(" / ")[0][:-2]
        if len(p_height) > 2 :
            height_list.append(p_height)
        else :
            height_list.append("None")

        p_weight = soup.find('div', class_="playerviw wbg r20").find('dl').text.split("\n")[4].split(" / ")[1][:-2]
        if len(p_weight) > 1 :
            weight_list.append(p_weight)
        else :
            weight_list.append("None")

        if len(soup.find('div', class_="playerviw wbg r20").find('dl').text.split("\n")) > 6 :
            school_list1 = []
            for p_school in soup.find('div', class_="playerviw wbg r20").find('dl').text.split("\n")[6].replace(" ","").split("-") :
                for p_school2 in p_school.split("/") :
                    school_list1.append(p_school2)
            school_list.append(school_list1)
        else :
            school_list.append('None')
        # breakpoint()
        p_draft = [x.text.replace("\xa0","").replace("  "," ") for x in soup.find('div', class_='career_box').find_all('li')]
        draft_list.append(p_draft)

        if soup.find('div', class_="tbl wbg r20") != None :
            for texts in [x.text for x in soup.find('div', class_="tbl wbg r20").find_all('tr')][1:] :
                texts = texts.split("\n")
                col1.append(texts[1])
                col2.append(texts[2])



        if soup.find('div', class_="swiptbl") != None :
            for dat in soup.find('div', class_="swiptbl").find_all('tbody') :
                for dat2 in dat.find_all('tr') :
                    col0.append(name_list[code_list.index(code)])
                    col3.append(dat2.find_all('td')[0].text)
                    col4.append(dat2.find_all('td')[1].text)
                    col5.append(dat2.find_all('td')[2].text)
                    col6.append(dat2.find_all('td')[3].text)
                    col7.append(dat2.find_all('td')[4].text)
                    col8.append(dat2.find_all('td')[5].text)
                    col9.append(dat2.find_all('td')[6].text)
                    col10.append(dat2.find_all('td')[7].text)
                    col11.append(dat2.find_all('td')[8].text)
                    col12.append(dat2.find_all('td')[9].text)
                    col13.append(dat2.find_all('td')[10].text)
                    col14.append(dat2.find_all('td')[11].text)


        center1_list = []
        center2_list = []

        if soup.find_all('div', class_="pchart wbg center r20 mt30") != None :
            for dat in soup.find_all('div', class_="pchart wbg center r20 mt30") :
                center1_list.append(dat.find_all('div', class_="chart-center")[0].text[:-1])
                center2_list.append(dat.find_all('div', class_="chart-center")[1].text[:-1])



        if soup.find('div', class_="swiper mt20") != None:
            for dat in soup.find_all('div', class_="swiper mt20")[0].find_all('tbody') :
                attack_col0.append(name_list[code_list.index(code)])
                attack_col1.append(dat.find_all('td')[0].text)
                attack_col2.append(dat.find_all('td')[1].text)
                attack_col3.append(dat.find_all('td')[2].text)
                attack_col4.append(dat.find_all('td')[3].text)
                attack_col5.append(dat.find_all('td')[4].text[:-1])
                attack_col6.append(dat.find_all('td')[5].text[:-1])
                attack_col7.append(center1_list[0])
                attack_col8.append(center2_list[0])



        if soup.find('div', class_="swiper mt20") != None :
            for dat in soup.find_all('div', class_="swiper mt20")[1].find_all('tbody') :
                block_col0.append(name_list[code_list.index(code)])
                block_col1.append(dat.find_all('td')[0].text)
                block_col2.append(dat.find_all('td')[1].text)
                block_col3.append(dat.find_all('td')[2].text)
                block_col4.append(dat.find_all('td')[3].text)
                block_col5.append(dat.find_all('td')[4].text)
                block_col6.append(dat.find_all('td')[5].text)
                block_col7.append(dat.find_all('td')[6].text[:-1])
                block_col8.append(center1_list[1])
                block_col9.append(center2_list[1])



        if soup.find('div', class_="swiper mt20") != None :
            for dat in soup.find_all('div', class_="swiper mt20")[2].find_all('tbody') :
                sub_col0.append(name_list[code_list.index(code)])
                sub_col1.append(dat.find_all('td')[0].text)
                sub_col2.append(dat.find_all('td')[1].text)
                sub_col3.append(dat.find_all('td')[2].text)
                sub_col4.append(dat.find_all('td')[3].text)
                sub_col5.append(dat.find_all('td')[4].text[:-1])
                sub_col6.append(center1_list[2])
                sub_col7.append(center2_list[2])



        if soup.find('div', class_="swiper mt20") != None :
            for dat in soup.find_all('div', class_="swiper mt20")[3].find_all('tbody') :
                set_col0.append(name_list[code_list.index(code)])
                set_col1.append(dat.find_all('td')[0].text)
                set_col2.append(dat.find_all('td')[1].text)
                set_col3.append(dat.find_all('td')[2].text)
                set_col4.append(dat.find_all('td')[3].text)
                set_col5.append(dat.find_all('td')[4].text[:-1])
                set_col6.append(center1_list[3])
                set_col7.append(center2_list[3])



        if soup.find('div', class_="swiper mt20") != None :
            for dat in soup.find_all('div', class_="swiper mt20")[4].find_all('tbody') :
                recieve_col0.append(name_list[code_list.index(code)])
                recieve_col1.append(dat.find_all('td')[0].text)
                recieve_col2.append(dat.find_all('td')[1].text)
                recieve_col3.append(dat.find_all('td')[2].text)
                recieve_col4.append(dat.find_all('td')[3].text[:-1])
                recieve_col5.append(dat.find_all('td')[4].text[:-1])
                recieve_col6.append(center1_list[4])
                recieve_col7.append(center2_list[4])



        if soup.find('div', class_="swiper mt20") != None :
            for dat in soup.find_all('div', class_="swiper mt20")[5].find_all('tbody') :
                dig_col0.append(name_list[code_list.index(code)])
                dig_col1.append(dat.find_all('td')[0].text)
                dig_col2.append(dat.find_all('td')[1].text)
                dig_col3.append(dat.find_all('td')[2].text)
                dig_col4.append(dat.find_all('td')[3].text)
                dig_col5.append(dat.find_all('td')[4].text[:-1])
                dig_col6.append(center1_list[5])
                dig_col7.append(center2_list[5])

        # 선수마다 리셋
        center1_list = []
        center2_list = []


        rank_text[p_name] = []
        if soup.find('div', class_="career wbg r20 kor mt20") != None :
            for dat in soup.find('div', class_="career wbg r20 kor mt20").find_all('dl') :
                dat_list = []
                for dat2 in dat.find_all('dd') :
                    if '\xa0' in dat2.text :
                        dat2 = dat2.text.replace('\xa0','')
                        # print(dat2)
                        if '\n' in dat2 :
                            dat2 = dat2.replace('\n','').replace('        ',' ').split('- ')
                            for dat3 in dat2 :
                                if len(dat3) > 2 :
                                    if dat3 not in dat_list :
                                        dat_list.append(dat3)
                        else :
                            dat_list.append(dat2)
                    else :
                        dat_list.append(dat2.text)
                rank_text[p_name].append({dat.find('dt').text : dat_list})





            if soup.find('div', class_='gallery r20 mt20') != None :
                dat_list = []
                for dat in soup.find('div', class_='gallery r20 mt20').find_all('img') :
                    name = name_list[code_list.index(code)]
                    dat_list.append(dat['src'])
                    photo_list[name] = dat_list



def get_all() :
    get_player_list()
    get_data()


#################체크하기
get_all()



df_profile = list(zip(main_photo_list, name_list, team_list, sex_list, kinds_list, code_list, position_list, birth_list, weight_list, height_list, school_list, draft_list))
df_season = list(zip(col0,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13,col14))
df_attack = list(zip(attack_col0,attack_col1,attack_col2,attack_col3,attack_col4,attack_col5,attack_col6))
df_block = list(zip(block_col0,block_col1,block_col2,block_col3,block_col4,block_col5,block_col6,block_col7,block_col8))
df_sub = list(zip(sub_col0,sub_col1,sub_col2,sub_col3,sub_col4,sub_col5,sub_col6))
df_set = list(zip(set_col0,set_col1,set_col2,set_col3,set_col4,set_col5,set_col6))
df_recieve = list(zip(recieve_col0,recieve_col1,recieve_col2,recieve_col3,recieve_col4,recieve_col5,recieve_col6))
df_dig = list(zip(dig_col0,dig_col1,dig_col2,dig_col3,dig_col4,dig_col5,dig_col6))
# 이것은 그 자체로 써야함 (rank_text, photo_list)
# breakpoint()


host = 'castor.db.elephantsql.com'
user = 'bqhqexud'
password = '2vzimQTD3IYUYsFjsoZpha5YOJRrydx6'
database = 'bqhqexud'

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cur = connection.cursor()


def db_update() :

    cur.execute("DROP TABLE IF EXISTS profile;")
    cur.execute(f"""CREATE TABLE profile (
        {profile_name[0]} VARCHAR,
        {profile_name[1]} VARCHAR,
        {profile_name[2]} VARCHAR,
        {profile_name[3]} VARCHAR,
        {profile_name[4]} VARCHAR,
        {profile_name[5]} VARCHAR,
        {profile_name[6]} VARCHAR,
        {profile_name[7]} VARCHAR,
        {profile_name[8]} VARCHAR,
        {profile_name[9]} VARCHAR,
        {profile_name[10]} VARCHAR,
        {profile_name[11]} VARCHAR
        );""")


    # df_profile = list(zip('1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'))
    # print(df_profile)
    for dat in df_profile :
        cur.execute(f"INSERT INTO profile ({profile_name[0]},{profile_name[1]},{profile_name[2]},{profile_name[3]},{profile_name[4]},{profile_name[5]},{profile_name[6]},{profile_name[7]},{profile_name[8]},{profile_name[9]},{profile_name[10]},{profile_name[11]}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", dat)


    cur.execute("DROP TABLE IF EXISTS season;")
    cur.execute(f"""CREATE TABLE season (
        {col_name[0]} VARCHAR,
        {col_name[1]} VARCHAR,
        {col_name[2]} VARCHAR,
        {col_name[3]} VARCHAR,
        {col_name[4]} INTEGER,
        {col_name[5]} INTEGER,
        {col_name[6]} INTEGER,
        {col_name[7]} FLOAT,
        {col_name[8]} FLOAT,
        {col_name[9]} FLOAT,
        {col_name[10]} FLOAT,
        {col_name[11]} FLOAT,
        {col_name[12]} FLOAT,
        {col_name[13]} INTEGER,
        {col_name[14]} INTEGER
        );""")


    # df_profile = list(zip('1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'))
    # print(df_profile)
    for dat in df_season :
        cur.execute(f"INSERT INTO season ({col_name[0]},{col_name[1]},{col_name[2]},{col_name[3]},{col_name[4]},{col_name[5]},{col_name[6]},{col_name[7]},{col_name[8]},{col_name[9]},{col_name[10]},{col_name[11]},{col_name[12]},{col_name[13]},{col_name[14]}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", dat)




    cur.execute("DROP TABLE IF EXISTS attack;")
    cur.execute(f"""CREATE TABLE attack (
        {attack_col_name[0]} VARCHAR,
        {attack_col_name[1]} INTEGER,
        {attack_col_name[2]} INTEGER,
        {attack_col_name[3]} INTEGER,
        {attack_col_name[4]} INTEGER,
        {attack_col_name[5]} FLOAT,
        {attack_col_name[6]} FLOAT
        );""")


    # df_profile = list(zip('1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'))
    # print(df_profile)
    for dat in df_attack :
        cur.execute(f"INSERT INTO attack ({attack_col_name[0]},{attack_col_name[1]},{attack_col_name[2]},{attack_col_name[3]},{attack_col_name[4]},{attack_col_name[5]},{attack_col_name[6]}) VALUES (%s,%s,%s,%s,%s,%s,%s);", dat)



    cur.execute("DROP TABLE IF EXISTS block;")
    cur.execute(f"""CREATE TABLE block (
        {block_col_name[0]} VARCHAR,
        {block_col_name[1]} INTEGER,
        {block_col_name[2]} INTEGER,
        {block_col_name[3]} INTEGER,
        {block_col_name[4]} INTEGER,
        {block_col_name[5]} INTEGER,
        {block_col_name[6]} FLOAT,
        {block_col_name[7]} FLOAT,
        {block_col_name[8]} FLOAT
        );""")


    # df_profile = list(zip('1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'))
    # print(df_profile)
    for dat in df_block :
        cur.execute(f"INSERT INTO block ({block_col_name[0]},{block_col_name[1]},{block_col_name[2]},{block_col_name[3]},{block_col_name[4]},{block_col_name[5]},{block_col_name[6]},{block_col_name[7]},{block_col_name[8]}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);", dat)



    cur.execute("DROP TABLE IF EXISTS sub;")
    cur.execute(f"""CREATE TABLE sub (
        {sub_col_name[0]} VARCHAR,
        {sub_col_name[1]} INTEGER,
        {sub_col_name[2]} INTEGER,
        {sub_col_name[3]} INTEGER,
        {sub_col_name[4]} FLOAT,
        {sub_col_name[5]} FLOAT,
        {sub_col_name[6]} FLOAT
        );""")


    # df_profile = list(zip('1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'))
    # print(df_profile)
    for dat in df_sub :
        cur.execute(f"INSERT INTO sub ({sub_col_name[0]},{sub_col_name[1]},{sub_col_name[2]},{sub_col_name[3]},{sub_col_name[4]},{sub_col_name[5]},{sub_col_name[6]}) VALUES (%s,%s,%s,%s,%s,%s,%s);", dat)





    cur.execute("DROP TABLE IF EXISTS set;")
    cur.execute(f"""CREATE TABLE set (
        {set_col_name[0]} VARCHAR,
        {set_col_name[1]} INTEGER,
        {set_col_name[2]} INTEGER,
        {set_col_name[3]} INTEGER,
        {set_col_name[4]} FLOAT,
        {set_col_name[5]} FLOAT,
        {set_col_name[6]} FLOAT
        );""")


    # df_profile = list(zip('1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'))
    # print(df_profile)
    for dat in df_set :
        cur.execute(f"INSERT INTO set ({set_col_name[0]},{set_col_name[1]},{set_col_name[2]},{set_col_name[3]},{set_col_name[4]},{set_col_name[5]},{set_col_name[6]}) VALUES (%s,%s,%s,%s,%s,%s,%s);", dat)




    cur.execute("DROP TABLE IF EXISTS recieve;")
    cur.execute(f"""CREATE TABLE recieve (
        {recieve_col_name[0]} VARCHAR,
        {recieve_col_name[1]} INTEGER,
        {recieve_col_name[2]} INTEGER,
        {recieve_col_name[3]} INTEGER,
        {recieve_col_name[4]} FLOAT,
        {recieve_col_name[5]} FLOAT,
        {recieve_col_name[6]} FLOAT
        );""")


    # df_profile = list(zip('1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'))
    # print(df_profile)
    for dat in df_recieve :
        cur.execute(f"INSERT INTO recieve ({recieve_col_name[0]},{recieve_col_name[1]},{recieve_col_name[2]},{recieve_col_name[3]},{recieve_col_name[4]},{recieve_col_name[5]},{recieve_col_name[6]}) VALUES (%s,%s,%s,%s,%s,%s,%s);", dat)




    cur.execute("DROP TABLE IF EXISTS dig;")
    cur.execute(f"""CREATE TABLE dig (
        {dig_col_name[0]} VARCHAR,
        {dig_col_name[1]} INTEGER,
        {dig_col_name[2]} INTEGER,
        {dig_col_name[3]} INTEGER,
        {dig_col_name[4]} FLOAT,
        {dig_col_name[5]} FLOAT,
        {dig_col_name[6]} FLOAT
        );""")


    # df_profile = list(zip('1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'))
    # print(df_profile)
    for dat in df_dig :
        cur.execute(f"INSERT INTO dig ({dig_col_name[0]},{dig_col_name[1]},{dig_col_name[2]},{dig_col_name[3]},{dig_col_name[4]},{dig_col_name[5]},{dig_col_name[6]}) VALUES (%s,%s,%s,%s,%s,%s,%s);", dat)

    #엄청 중요한 커밋 !!
    connection.commit()


def rank_update() :

    HOST = 'cluster0.ukjxr.mongodb.net'
    USER = 'sasohangamsung'
    PASSWORD = '1218'
    DATABASE_NAME = 'myFirstDatabase'
    COLLECTION_NAME = 'rank_text'
    mongo_url = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

    client = MongoClient(mongo_url)
    database = client[DATABASE_NAME]
    collection = database[COLLECTION_NAME]

    collection.drop()
    collection.insert_one(document=rank_text)

def photo_update() :

    HOST = 'cluster0.ukjxr.mongodb.net'
    USER = 'sasohangamsung'
    PASSWORD = '1218'
    DATABASE_NAME = 'myFirstDatabase'
    COLLECTION_NAME = 'photo_list'
    mongo_url = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

    client = MongoClient(mongo_url)
    database = client[DATABASE_NAME]
    collection = database[COLLECTION_NAME]

    collection.drop()
    collection.insert_one(document=photo_list)


def pickle_save() :
    with open("df_profile.pickle","wb") as aa1:
        pickle.dump(df_profile, aa1)

    with open("df_season.pickle","wb") as aa2:
        pickle.dump(df_season, aa2)

    with open("df_attack.pickle","wb") as aa3:
        pickle.dump(df_attack, aa3)

    with open("df_block.pickle","wb") as aa4:
        pickle.dump(df_block, aa4)

    with open("df_sub.pickle","wb") as aa5:
        pickle.dump(df_sub, aa5)

    with open("df_set.pickle","wb") as aa6:
        pickle.dump(df_set, aa6)

    with open("df_recieve.pickle","wb") as aa7:
        pickle.dump(df_recieve, aa7)

    with open("df_dig.pickle","wb") as aa8:
        pickle.dump(df_dig, aa8)

    with open("rank_text.pickle","wb") as aa9:
        pickle.dump(rank_text, aa9)

    with open("photo_list.pickle","wb") as aa10:
        pickle.dump(photo_list, aa10)




db_update()
rank_update()
photo_update()
pickle_save()


# db_update()



# breakpoint()

# # KST 기반으로 실행하는 방법
# scheduler = BlockingScheduler({'apscheduler.timezone':'Asia/seoul'})
# scheduler.add_job(func=get_all(), hour='5', id="get_all")

# 테스트용
# url = 'https://m.kovo.co.kr/team/21222_player_view.asp?p_code=0001343&t_code=2001&'

# page = requests.get(url)
# soup = BeautifulSoup(page.content, 'html.parser')

