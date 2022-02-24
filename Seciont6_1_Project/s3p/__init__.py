from flask import Flask, jsonify, render_template, request	#플라스크 관련
import pickle
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta


FILEPATH1 = os.path.join(os.getcwd(), 's3p', 'model_pipe.pickle')
FILEPATH2 = os.path.join(os.getcwd(), 's3p', 'df_season.pickle')
FILEPATH3 = os.path.join(os.getcwd(), 's3p', 'df_attack.pickle')
FILEPATH4 = os.path.join(os.getcwd(), 's3p', 'df_block.pickle')
FILEPATH5 = os.path.join(os.getcwd(), 's3p', 'df_dig.pickle')
FILEPATH6 = os.path.join(os.getcwd(), 's3p', 'df_recieve.pickle')
FILEPATH7 = os.path.join(os.getcwd(), 's3p', 'df_set.pickle')
FILEPATH8 = os.path.join(os.getcwd(), 's3p', 'df_sub.pickle')
FILEPATH9 = os.path.join(os.getcwd(), 's3p', 'rank_text.pickle')
FILEPATH10 = os.path.join(os.getcwd(), 's3p', 'X_train.pickle')
FILEPATH11 = os.path.join(os.getcwd(), 's3p', 'y_train.pickle')
# FILEPATH12 = os.path.join(os.getcwd(), 's3p', 'sim_df.pickle')
FILEPATH13 = os.path.join(os.getcwd(), 's3p', 'df_profile_train.pickle')
FILEPATH14 = os.path.join(os.getcwd(), 's3p', 'df_profile_rev1.pickle')

with open(FILEPATH1,"rb") as dd:
    pipe = pickle.load(dd)

with open(FILEPATH2,"rb") as dd0:
    df_season = pickle.load(dd0)

with open(FILEPATH3,"rb") as dd1:
    df_attack = pickle.load(dd1)

with open(FILEPATH4,"rb") as dd2:
    df_block = pickle.load(dd2)

with open(FILEPATH5,"rb") as dd3:
    df_dig = pickle.load(dd3)

with open(FILEPATH6,"rb") as dd4:
    df_recieve = pickle.load(dd4)

with open(FILEPATH7,"rb") as dd5:
    df_set = pickle.load(dd5)

with open(FILEPATH8,"rb") as dd6:
    df_sub = pickle.load(dd6)

with open(FILEPATH9,"rb") as dd7:
    rank_text = pickle.load(dd7)

with open(FILEPATH10,"rb") as dd8:
    X_train = pickle.load(dd8)

with open(FILEPATH11,"rb") as dd9:
    y_train = pickle.load(dd9)

# with open(FILEPATH12,"rb") as dd10:
    # sim_df = pickle.load(dd10)

with open(FILEPATH13,"rb") as dd11:
    df_profile_train = pickle.load(dd11)

with open(FILEPATH14,"rb") as dd12:
    df_profile_all = pickle.load(dd12)

def create_app():
    app = Flask(__name__)

    return app

app = create_app()


@app.route('/')
def call_API():
    return render_template('main.html')

@app.route('/post', methods=['GET','POST'])
def post():
    if request.method == 'POST':

        age = request.form['age']
        age = str(age)
        sex = request.form['sex']
        sex = str(sex)
        kinds = request.form['kinds']
        kinds = str(kinds)
        position = request.form['position']
        position = str(position)
        weight_class = request.form['weight_class']
        weight_class = str(weight_class)
        height_class = request.form['height_class']
        height_class = str(height_class)
        birth_month_4 = request.form['birth(month)_4']
        birth_month_4 = str(birth_month_4)
        birth_day_4 = request.form['birth(day)_4']
        birth_day_4 = str(birth_day_4)
        school_last = request.form['school_last']
        school_last = str(school_last)

        if age != 'None1' :
            z1 = df_profile_train['age'] == age
        else :
            z1 = df_profile_train['age'] != age

        if sex != 'None1' :
            z2 = df_profile_train['sex'] == sex
            zz2 = df_profile_all['sex'] == sex
        else :
            z2 = df_profile_train['sex'] != sex
            zz2 = df_profile_all['sex'] != sex

        if kinds != 'None1' :
            z3 = df_profile_train['kinds'] == kinds
            zz3 = df_profile_all['kinds'] == kinds
        else :
            z3 = df_profile_train['kinds'] != kinds
            zz3 = df_profile_all['kinds'] != kinds

        if position != 'None1' :
            z4 = df_profile_train['position'] == position
            zz4 = df_profile_all['position'] == position
        else :
            z4 = df_profile_train['position'] != position
            zz4 = df_profile_all['position'] != position

        if weight_class != 'None1' :
            z5 = df_profile_train['weight_class'] == weight_class
        else :
            z5 = df_profile_train['weight_class'] != weight_class

        if height_class != 'None1' :
            z6 = df_profile_train['height_class'] == height_class
        else :
            z6 = df_profile_train['height_class'] != height_class

        if birth_month_4 != 'None1' :
            z7 = df_profile_train['birth(month)_4'] == birth_month_4
        else :
            z7 = df_profile_train['birth(month)_4'] != birth_month_4

        if birth_day_4 != 'None1' :
            z8 = df_profile_train['birth(day)_4'] == birth_day_4
        else :
            z8 = df_profile_train['birth(day)_4'] != birth_day_4

        if school_last != 'None1' :
            z9 = df_profile_train['school_last'] == school_last
        else :
            z9 = df_profile_train['school_last'] != school_last

        a_name_list = []
        for a_name in df_profile_train[z1 & z2 & z3 & z4 & z5 & z6 & z7 & z8 & z9]['name'] :
            a_name_list.append(a_name)

        if len(a_name_list) == 0 :
            message = '조건에 해당하는 선수가 없습니다!'
            result = a_name_list
        
        elif len(a_name_list) == 1 :
            message = '조건에 맞는 단 한명 !'
            result = a_name_list
        else :
            message = f'{len(a_name_list)}명 중에 있을지도 ...'
            result = a_name_list

        message2 = '이름을 클릭하면, 공식배구연맹 선수정보 사이트로 이동합니다.'
        zip_list = []
        # for num in range(len(a_name_list)) :
        #     zo = df_profile_all['name'] == a_name_list[num]
        #     for url in df_profile_all[zo]['code'] :
        #         url = 'https://m.kovo.co.kr/team/'+url
        #         zip_list.append((a_name_list[num],url))

                
        for num in range(len(a_name_list)) :
            zo = df_profile_all['name'] == a_name_list[num]
            for url, photo in zip(df_profile_all[zo]['code'], df_profile_all[zo]['main_photo']):
                url = 'https://m.kovo.co.kr/team/'+url
                zip_list.append((a_name_list[num],url,photo))
        

        # result = [age,sex,kinds,position,weight_class,height_class,birth_month_4,birth_day_4,school_last]

        df_sim = df_profile_all[zz2 & zz3 & zz4][['name', 'weight', 'height', 'birth(year)']]
        df_sim['weight'] = df_sim['weight'].replace('None',None).astype('int')
        df_sim['height'] = df_sim['height'].replace('None',None).astype('int')
        df_sim['birth(year)'] = df_sim['birth(year)'].replace('None',None).astype('int')
        
        if weight_class != "None1" :
            weight_min = int(weight_class.split(" ")[0][:-2])-10
            if len(weight_class.split(" ")) > 1 :
                weight_max = int(weight_class.split(" ")[1][:-2])+10
            else :
                weight_max = int(weight_class.split(" ")[0][:-2])+20
        else :
            weight_min = 0
            weight_max = 0
        
        if height_class != "None1" :
            height_min = int(height_class.split(" ")[0][:-2])-10
            if len(height_class.split(" ")) > 1 :
                height_max = int(height_class.split(" ")[1][:-2])+10
            else :
                height_max = int(height_class.split(" ")[0][:-2])+20
        else :
            height_min = 0
            height_max = 0
        
        if age != "None1" :
            age_min = int(age.split(" ")[0][:-2])-10
            if len(age.split(" ")) > 1 :
                age_max = int(age.split(" ")[1][:-2])+10
            else :
                age_max = int(age.split(" ")[0][:-2])+20
        else :
            age_min = 0
            age_max = 0
        

        zzz1 = df_sim['weight'] >= weight_min
        zzz2 = df_sim['weight'] < weight_min+10
        zzz7 = df_sim['weight'] >= weight_max
        zzz8 = df_sim['weight'] < weight_max+10
        zzz3 = df_sim['height'] >= height_min
        zzz4 = df_sim['height'] < height_min+10
        zzz9 = df_sim['height'] >= height_max
        zzz10 = df_sim['height'] < height_max+10
        zzz5 = df_sim['birth(year)'] >= datetime.today().year-age_min
        zzz6 = df_sim['birth(year)'] < datetime.today().year-age_min+10
        zzz11 = df_sim['birth(year)'] >= datetime.today().year-age_max
        zzz12 = df_sim['birth(year)'] < datetime.today().year-age_max+10


        df_sim2 = df_sim[(zzz1 & zzz2) | (zzz3 & zzz4) | (zzz5 & zzz6) | (zzz7 & zzz8) | (zzz9 & zzz10) | (zzz11 & zzz12)]
        # similarity = cosine_similarity(df_sim.drop('name',axis=1))
        # sim_df = pd.DataFrame(similarity, index=df_sim['name'], columns=df_sim['name'])
        re_list = []
        for name in df_sim2['name'] :
            zo = df_profile_all['name'] == name
            for url, photo in zip(df_profile_all[zo]['code'],df_profile_all[zo]['main_photo']) :
                url = 'https://m.kovo.co.kr/team/'+url
                re_list.append((name,url,photo))

        # print(re_list)
        re_comment = '검색하신 조건과 유사한 선수 목록'
    return render_template('result.html', result = result, message = message,
                           zip_list = zip_list, message2 = message2, re_list = re_list,
                           re_comment = re_comment)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


