import pickle
import pandas as pd
from datetime import datetime, timedelta
import psycopg2
from pymongo import MongoClient

with open("df_profile.pickle","rb") as aa1:
    df_profile = pickle.load(aa1)
with open("df_season.pickle","rb") as aa2:
    df_season = pickle.load(aa2)
with open("df_attack.pickle","rb") as aa3:
    df_attack = pickle.load(aa3)
with open("df_block.pickle","rb") as aa4:
    df_block = pickle.load(aa4)
with open("df_sub.pickle","rb") as aa5:
    df_sub = pickle.load(aa5)
with open("df_set.pickle","rb") as aa6:
    df_set = pickle.load(aa6)
with open("df_recieve.pickle","rb") as aa7:
    df_recieve = pickle.load(aa7)
with open("df_dig.pickle","rb") as aa8:
    df_dig = pickle.load(aa8)
with open("rank_text.pickle","rb") as aa9:
    rank_text = pickle.load(aa9)
with open("photo_list.pickle","rb") as aa10:
    photo_list = pickle.load(aa10)

profile_name = ['main_photo', 'name', 'team', 'sex', 'kinds', 'code', 'position', 'birthday', 'weight', 'height', 'school', 'draft']
col_name = ['이름', '경기구분', '시즌구분', '팀구분', '경기_수', '세트_수', '득점', '공격종합_성공률', '블로킹Avg_set', '서브Avg_set', '세트Avg_set', '리시브효율', '디그Avg_set', '벌칙', '범실']
attack_col_name = ['이름', '공격_시도','공격_성공','범실','상대_블럭','성공률','점유율']
block_col_name = ['이름','블로킹_시도','블로킹_성공','유효_블로킹','범실','실패','세트당_개수','점유율','성공률']
sub_col_name = ['이름','서브_시도','서브_성공','범실','세트당_개수','점유율','성공률']
set_col_name = ['이름','세트_시도','세트_성공','범실','세트당_개수','점유율','성공률']
recieve_col_name = ['이름','리시브_시도','리시브_정확','리시브_실패','리시브_효율','점유율','성공률']
dig_col_name = ['이름','디그_시도','디그_정확','디그_실패','세트당_개수','점유율','성공률']


df_profile_rev = pd.DataFrame(df_profile, columns = profile_name)
df_season_rev = pd.DataFrame(df_season, columns = col_name)
df_attack_rev = pd.DataFrame(df_attack, columns = attack_col_name)
df_block_rev = pd.DataFrame(df_block, columns = block_col_name)
df_sub_rev = pd.DataFrame(df_sub, columns = sub_col_name)
df_set_rev = pd.DataFrame(df_set, columns = set_col_name)
df_recieve_rev = pd.DataFrame(df_recieve, columns = recieve_col_name)
df_dig_rev = pd.DataFrame(df_dig, columns = dig_col_name)


df_profile_rev['sex'] = df_profile_rev['sex'].replace(1,'남자').replace(2,'여자')
df_profile_rev['kinds'] = df_profile_rev['kinds'].replace(1,'현역선수').replace(2,'기타선수').replace(3,'은퇴선수').replace(4,'외국인선수')
df_profile_rev['position'] = df_profile_rev['position'].replace('L','레프트').replace('R','라이트').replace('C','센터').replace('S','세터').replace('Li','리베로')

school_list_1 = []
school_list_2 = []
school_list_3 = []
school_list_4 = []

for line in df_profile_rev['school'] :
    if line == "None" :
        school_list_1.append("None")
        school_list_2.append("None")
        school_list_3.append("None")
        school_list_4.append("None")
    elif len(line) == 4 :
        school_list_1.append(line[0])
        school_list_2.append(line[1])
        school_list_3.append(line[2])
        school_list_4.append(line[3])
    elif len(line) == 3 :
        school_list_1.append("None")
        school_list_2.append(line[0])
        school_list_3.append(line[1])
        school_list_4.append(line[2])
    elif len(line) == 2 :
        school_list_1.append("None")
        school_list_2.append("None")
        school_list_3.append(line[0])
        school_list_4.append(line[1])
    elif len(line) == 1 :
        school_list_1.append("None")
        school_list_2.append("None")
        school_list_3.append("None")
        school_list_4.append(line[0])

df_profile_rev['school_1'] = school_list_1
df_profile_rev['school_2'] = school_list_2
df_profile_rev['school_3'] = school_list_3
df_profile_rev['school_4'] = school_list_4

birth_y = []
birth_m = []
birth_d = []

for birth in df_profile_rev['birthday']:
    if birth != "None" :
        birth = birth.split(" ")
        birth_y.append(birth[0][:-1])
        birth_m.append(birth[1][:-1])
        birth_d.append(birth[2][:-1])
    else :
        birth_y.append("None")
        birth_m.append("None")
        birth_d.append("None")

df_profile_rev['birth(year)'] = birth_y
df_profile_rev['birth(month)'] = birth_m
df_profile_rev['birth(day)'] = birth_d

# print(df_profile_rev.columns)




weight_list1 = []
for weight in df_profile_rev['weight'] :
    if weight != "None" :
        weight = int(weight)
        if weight >= 40 and weight < 50 :
            weight_list1.append("40이상 50미만")
        elif weight >= 50 and weight < 60 :
            weight_list1.append("50이상 60미만")
        elif weight >= 60 and weight < 70 :
            weight_list1.append("60이상 70미만")
        elif weight >= 70 and weight < 80 :
            weight_list1.append("70이상 80미만")
        elif weight >= 80 and weight < 90 :
            weight_list1.append("80이상 90미만")
        elif weight >= 90 and weight < 100 :
            weight_list1.append("90이상 100미만")
        elif weight >= 100 and weight < 110 :
            weight_list1.append("100이상 110미만")
        elif weight >= 110 and weight < 120 :
            weight_list1.append("110이상 120미만")
    else :
        weight_list1.append("None")


df_profile_rev['weight_class'] = weight_list1



height_list1 = []
for height in df_profile_rev['height'] :
    if height != "None" :
        height = int(height)
        if height < 160 :
            height_list1.append("160미만")
        elif height >= 155 and height < 160 :
            height_list1.append("155이상 160미만")
        elif height >= 160 and height < 165 :
            height_list1.append("160이상 165미만")
        elif height >= 165 and height < 170 :
            height_list1.append("165이상 170미만")
        elif height >= 170 and height < 175 :
            height_list1.append("170이상 175미만")
        elif height >= 175 and height < 180 :
            height_list1.append("175이상 180미만")
        elif height >= 180 and height < 185 :
            height_list1.append("180이상 185미만")
        elif height >= 185 and height < 190 :
            height_list1.append("185이상 190미만")
        elif height >= 190 and height < 195 :
            height_list1.append("190이상 195미만")
        elif height >= 195 and height < 200 :
            height_list1.append("195이상 200미만")
        elif height >= 200 and height < 205 :
            height_list1.append("200이상 205미만")
        elif height >= 205 and height < 210 :
            height_list1.append("205이상 210미만")
        elif height >= 210 :
            height_list1.append("210이상")

    else :
        height_list1.append("None")

df_profile_rev['height_class'] = height_list1



year_list1 = []
for year in df_profile_rev['birth(year)'] :
    if year != "None" :
        year = datetime.today().year - int(year)
        if year < 20 :
            year_list1.append("20미만")
        elif year >= 20 and year < 25 :
            year_list1.append("20이상 25미만")
        elif year >= 25 and year < 30 :
            year_list1.append("25이상 30미만")
        elif year >= 30 and year < 35 :
            year_list1.append("30이상 35미만")
        elif year >= 35 and year < 40 :
            year_list1.append("35이상 40미만")
        elif year >= 40 and year < 45 :
            year_list1.append("40이상")
        else :
            year_list1.append("None")
    else :
        year_list1.append("None")

df_profile_rev['age'] = year_list1


month_list1 = []
for month in df_profile_rev['birth(month)'] :
    if month != "None" :
        try :
            month = int(month)
        except :
            month = int(month[:-1])
        if  month >= 1 and month < 4 :
            month_list1.append("1월~3월")
        elif month >= 4 and month < 7 :
            month_list1.append("4월~6월")
        elif month >= 7 and month < 10 :
            month_list1.append("7월~9월")
        elif month >= 10 and month <= 12 :
            month_list1.append("10월~12월")

    else :
        month_list1.append("None")

df_profile_rev['birth(month)_4'] = month_list1



school_list1 = []
for school in df_profile_rev['school_4'] :
    if  school[-1] == "초" :
        school_list1.append("초등학교->프로")
    elif school[-1] == "중" :
        school_list1.append("중학교->프로")
    elif school[-1] == "고" or school[-1] == "상" :
        school_list1.append("고등학교->프로")
    elif school[-1] == "대" :
        school_list1.append("대학교->프로")
    else :
        school_list1.append("None")

df_profile_rev['school_last'] = school_list1



day_list1 = []
for day in df_profile_rev['birth(day)'] :
    if day != "None" :
        day = int(day)
        if  day >= 1 and day < 11 :
            day_list1.append("1일~10일")
        elif  day >= 11 and day < 21 :
            day_list1.append("11일~20일")
        elif  day >= 21 and day < 31 :
            day_list1.append("21일~31일")
        else :
            day_list1.append("None")
    else :
        day_list1.append("None")

df_profile_rev['birth(day)_4'] = day_list1



df_profile_rev1 = df_profile_rev[['main_photo', 'name', 'age', 'team', 'sex', 'kinds', 'code', 'position',
                                  'weight', 'height', 'draft', 'school_1', 'school_2', 'school_3',
                                  'school_4', 'school_last',
                                  'birth(year)', 'birth(month)', 'birth(month)_4', 'birth(day)', 'birth(day)_4',
                                  'weight_class','height_class']]

df_profile_rev2 = df_profile_rev[['main_photo', 'name', 'age', 'sex', 'birth(year)', 'birth(month)', 'birth(day)',
                                  'team', 'kinds', 'position', 'weight', 'height',
                                  'school_1', 'school_2', 'school_3', 'school_4']]

df_profile_train = df_profile_rev[['name', 'age', 'team', 'sex', 'kinds', 'position', 'weight_class', 'height_class',
                                   'birth(year)', 'birth(month)', 'birth(day)', 'birth(month)_4', 'birth(day)_4',
                                   'school_1', 'school_2', 'school_3', 'school_4', 'school_last']]



# df_attack_rev = df_attack_rev.drop(['성공률1','점유율1'], axis=1)
# df_block_rev = df_block_rev.drop(['점유율1'], axis=1)
# df_sub_rev = df_sub_rev.drop(['점유율1'], axis=1)
# df_set_rev = df_set_rev.drop(['점유율1'], axis=1)
# df_recieve_rev = df_recieve_rev.drop(['점유율1'], axis=1)
# df_dig_rev = df_dig_rev.drop(['점유율1'], axis=1)



df_attack_rev['공격_시도'] = df_attack_rev['공격_시도'].astype(int)
df_attack_rev['공격_성공'] = df_attack_rev['공격_성공'].astype(int)
df_attack_rev['범실'] = df_attack_rev['범실'].astype(int)
df_attack_rev['상대_블럭'] = df_attack_rev['상대_블럭'].astype(int)
df_attack_rev['성공률'] = df_attack_rev['성공률'].astype(float)
df_attack_rev['점유율'] = df_attack_rev['점유율'].astype(float)

df_block_rev['블로킹_시도'] = df_block_rev['블로킹_시도'].astype(int)
df_block_rev['블로킹_성공'] = df_block_rev['블로킹_성공'].astype(int)
df_block_rev['유효_블로킹'] = df_block_rev['유효_블로킹'].astype(int)
df_block_rev['범실'] = df_block_rev['범실'].astype(int)
df_block_rev['실패'] = df_block_rev['실패'].astype(int)
df_block_rev['세트당_개수'] = df_block_rev['세트당_개수'].astype(float)
df_block_rev['점유율'] = df_block_rev['점유율'].astype(float)
df_block_rev['성공률'] = df_block_rev['성공률'].astype(float)

df_sub_rev['서브_시도'] = df_sub_rev['서브_시도'].astype(int)
df_sub_rev['서브_성공'] = df_sub_rev['서브_성공'].astype(int)
df_sub_rev['범실'] = df_sub_rev['범실'].astype(int)
df_sub_rev['세트당_개수'] = df_sub_rev['세트당_개수'].astype(float)
df_sub_rev['점유율'] = df_sub_rev['점유율'].astype(float)
df_sub_rev['성공률'] = df_sub_rev['성공률'].astype(float)

df_set_rev['세트_시도'] = df_set_rev['세트_시도'].astype(int)
df_set_rev['세트_성공'] = df_set_rev['세트_성공'].astype(int)
df_set_rev['범실'] = df_set_rev['범실'].astype(int)
df_set_rev['세트당_개수'] = df_set_rev['세트당_개수'].astype(float)
df_set_rev['점유율'] = df_set_rev['점유율'].astype(float)
df_set_rev['성공률'] = df_set_rev['성공률'].astype(float)

df_recieve_rev['리시브_시도'] = df_recieve_rev['리시브_시도'].astype(int)
df_recieve_rev['리시브_정확'] = df_recieve_rev['리시브_정확'].astype(int)
df_recieve_rev['리시브_실패'] = df_recieve_rev['리시브_실패'].astype(int)
df_recieve_rev['리시브_효율'] = df_recieve_rev['리시브_효율'].astype(float)
df_recieve_rev['점유율'] = df_recieve_rev['점유율'].astype(float)
df_recieve_rev['성공률'] = df_recieve_rev['성공률'].astype(float)

df_dig_rev['디그_시도'] = df_dig_rev['디그_시도'].astype(int)
df_dig_rev['디그_정확'] = df_dig_rev['디그_정확'].astype(int)
df_dig_rev['디그_실패'] = df_dig_rev['디그_실패'].astype(int)
df_dig_rev['세트당_개수'] = df_dig_rev['세트당_개수'].astype(float)
df_dig_rev['점유율'] = df_dig_rev['점유율'].astype(float)
df_dig_rev['성공률'] = df_dig_rev['성공률'].astype(float)



with open("df_profile_rev1.pickle","wb") as bb0:
    pickle.dump(df_profile_rev1, bb0)

with open("df_profile_train.pickle","wb") as bb1:
    pickle.dump(df_profile_train, bb1)

with open("df_profile_rev2.pickle","wb") as bb2:
    pickle.dump(df_profile_rev2, bb2)

# print(df_profile_train.dtypes)
# breakpoint()
