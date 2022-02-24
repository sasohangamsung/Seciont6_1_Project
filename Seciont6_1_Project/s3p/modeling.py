import pickle
import pandas as pd
from category_encoders import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

with open("df_profile_train.pickle","rb") as aa1:
    df_profile_train = pickle.load(aa1)
    
with open("df_profile_rev1.pickle","rb") as aa2:
    df_profile_all = pickle.load(aa2)

# X_train = df_profile_train.drop(['team', 'school_4', 'name', 'birth(year)', 'birth(day)', 'birth(month)'],axis=1)
# X_train = df_profile_train.drop(['name', 'team', 'birth(year)', 'birth(month)', 'birth(day)'],axis=1)
# X_train = df_profile_train.drop(['team', 'name',
#                                  'birth(year)', 'birth(day)', 'birth(month)',
#                                  'school_1', 'school_2', 'school_3', 'school_4'],axis=1)
# X_train = df_profile_train.drop(['team', 'name',
#                                  'birth(year)', 'birth(day)', 'birth(month)',
#                                  'school_1', 'school_2', 'school_3', 'school_4'],axis=1)

X_train = df_profile_train.drop(['team', 'name',
                                 'birth(year)', 'birth(day)', 'birth(month)',
                                 'school_1', 'school_2', 'school_3', 'school_4'],axis=1)
# X_train = df_profile_train.drop(['name'], axis=1)
y_train = df_profile_train['name']


pipe = make_pipeline(
    OrdinalEncoder(),
    DecisionTreeClassifier(random_state=0, criterion='entropy')
)



# pipe.fit(X_train, y_train)





# print(X_train.iloc[182])
# print('훈련 정확도', pipe.score(X_train, y_train))
# print(df_profile_train[139:140])
# print('검증 정확도', pipe.score(test, y_train))
# print(df_profile_train.columns)
# print('검증 결과', pipe.predict(text_ex))
# print(test.columns)
# print(test.iloc[186:187])

#############특성중요도 확인#############
# model_dt = pipe.named_steps['decisiontreeclassifier']
# importances = pd.Series(model_dt.feature_importances_, X_train.columns)
# plt.figure(figsize=(10,5))
# importances.sort_values().plot.barh();
# plt.show()





# ordi = OrdinalEncoder()
# X_trans = ordi.fit_transform(X_train)
# similarity = cosine_similarity(X_trans)

# sim_df = pd.DataFrame(similarity, index=y_train, columns=y_train)
# print(sim_df['송원근'].sort_values(ascending=False).head(50))
# print(sim_df.head(10))
# print(X_train)
# print(X_train.columns)


# age = '25이상 30미만'
# sex = '남자'
# kinds = '현역선수'
# position = '센터'
# weight_class = '80이상 90미만'
# height_class = '195이상 200미만'
# birth_month_4 = '1월~3월'
# birth_day_4 = '21일~31일'
# school_last = '대학교->프로'


# # age = 'None1'
# # sex = 'None1'
# # kinds = 'None1'
# # position = 'None1'
# # weight_class = 'None1'
# # height_class = 'None1'
# # birth_month_4 = 'None1'
# # birth_day_4 = 'None1'
# # school_last = 'None1'

# if age != 'None1' :
#     z1 = df_profile_train['age'] == age
# else :
#     z1 = df_profile_train['age'] != age

# if sex != 'None1' :
#     z2 = df_profile_train['sex'] == sex
# else :
#     z2 = df_profile_train['sex'] != sex

# if kinds != 'None1' :
#     z3 = df_profile_train['kinds'] == kinds
# else :
#     z3 = df_profile_train['kinds'] != kinds

# if position != 'None1' :
#     z4 = df_profile_train['position'] == position
# else :
#     z4 = df_profile_train['position'] != position

# if weight_class != 'None1' :
#     z5 = df_profile_train['weight_class'] == weight_class
# else :
#     z5 = df_profile_train['weight_class'] != weight_class

# if height_class != 'None1' :
#     z6 = df_profile_train['height_class'] == height_class
# else :
#     z6 = df_profile_train['height_class'] != height_class

# if birth_month_4 != 'None1' :
#     z7 = df_profile_train['birth(month)_4'] == birth_month_4
# else :
#     z7 = df_profile_train['birth(month)_4'] != birth_month_4

# if birth_day_4 != 'None1' :
#     z8 = df_profile_train['birth(day)_4'] == birth_day_4
# else :
#     z8 = df_profile_train['birth(day)_4'] != birth_day_4

# if school_last != 'None1' :
#     z9 = df_profile_train['school_last'] == school_last
# else :
#     z9 = df_profile_train['school_last'] != school_last

# a_name_list = []
# for a_name in df_profile_train[z1 & z2 & z3 & z4 & z5 & z6 & z7 & z8 & z9]['name'] :
#     a_name_list.append(a_name)
# # print(X_trans)
# # print(df_profile_train[z1 & z2 & z3 & z4 & z5 & z6 & z7 & z8 & z9])
# # print(a_name_list)
# # print(y_train.iloc[346])
# # print(df_profile_train.iloc[351])
# # print(df_profile_all.iloc[351])
# print(df_profile_all.iloc[386])

with open("model_pipe.pickle","wb") as cc0:
    pickle.dump(pipe, cc0)

with open("test_columns.pickle","wb") as cc1:
    pickle.dump(X_train.columns, cc1)

with open("X_train.pickle","wb") as cc2:
    pickle.dump(X_train, cc2)

with open("y_train.pickle","wb") as cc3:
    pickle.dump(y_train, cc3)

# with open("sim_df.pickle","wb") as cc4:
#     pickle.dump(sim_df, cc4)
    
# print(df_profile_all.iloc[361])