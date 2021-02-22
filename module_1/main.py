import pandas as pd
import os
import numpy as np
import re

football = pd.read_csv('data_sf.xls')
# сумма зарплат в клубе Челси
s = football.groupby(['Club']).sum().loc['Chelsea']['Wage']

# максимальная зарплата Аргентинца в возрасте 20 лет
s = football[football.Nationality == 'Argentina'].groupby(['Club']).max().loc['FC Barcelona']['Strength']
# print(s)

df2 = football.pivot_table(columns='Position', index='Club', values='SprintSpeed', aggfunc='mean', fill_value=0)
# print(df2['ST'].sort_values(ascending=False))

rating = pd.read_csv('ratings.csv')
#print(rating[rating.rating == 0.5].count())

movies = pd.read_csv('movies.csv')
#print(movies['movieId'].nunique())
rate_merge = movies.merge(rating, how='outer', on='movieId')
# print(rate_merge[rate_merge.rating.isnull()])

items_dict = {
    'item_id': [417283, 849734, 132223, 573943, 19475, 3294095, 382043, 302948, 100132, 312394],
    'vendor': ['Samsung', 'LG', 'Apple', 'Apple', 'LG', 'Apple', 'Samsung', 'Samsung', 'LG', 'ZTE'],
    'stock_count': [54, 33, 122, 18, 102, 43, 77, 143, 60, 19]
}
purchase_log = {
    'purchase_id': [101, 101, 101, 112, 121, 145, 145, 145, 145, 221],
    'item_id': [417283, 849734, 132223, 573943, 19475, 3294095, 382043, 302948, 103845, 100132],
    'price': [13900, 5330, 38200, 49990, 9890, 33000, 67500, 34500, 89900, 11400]
}

items_df = pd.DataFrame(items_dict)
purchase_df = pd.DataFrame(purchase_log)

merge_df = items_df.merge(purchase_df, how='inner', on='item_id')
# print(merge_df.item_id.nunique())

value_df = pd.DataFrame(merge_df.price*merge_df.stock_count, columns=['value'])
merge_df = pd.concat([merge_df, value_df], axis=1)
# print(merge_df)

files = ['setup.py', 'ratings.txt', 'stock_stats.txt', 'movies.txt', 'run.sh', 'game_of_thrones.mov']
data = [x for x in files if x.find('txt') >= 0]
# print(data)

data = pd.DataFrame(columns = ['userId', 'movieId', 'rating', 'timestamp'])
for file in os.listdir('data'):
    temp = pd.read_csv('./data/' + file, names = ['userId', 'movieId', 'rating', 'timestamp'])
    data = pd.concat([data, temp])
#print(data)

sample = pd.read_csv('sample.xls')
columns = list(map(lambda x: x.lower(), sample.columns))
#print(sample)

users = pd.read_csv('users.xls',encoding='koi8_r',  sep='\t')
#print(sample.City.isnull())
log = pd.read_csv('log.xls')
log.columns = ['user_id', 'time', 'bet', 'win']

new_log = log[~log.user_id.str.contains('#error', na=False)]
#print(new_log.user_id.unique())


def age_category(age):
    # Ваш код ниже
    if age < 23:
        return 'молодой'
    if age > 35:
        return 'зрелый'
    return 'средний'

import re
# прочитаем файл в переменную log;
log = pd.read_csv("log.xls", header=None)
# добавим названия колонок user_id, time, bet, win;
log.columns = ['user_id', 'time', 'bet', 'win']

# удалим строки, которые содержат значения user_id с ошибками;
# log = log[log.user_id != '#error']
log = log[log.user_id.str.find('user_') >= 0]

# оставим в поле user_id значение типа: "user_N", где N значение идентификатора;
# pattern = re.compile('user_\d+')
# log.user_id = log.user_id.apply(lambda x: pattern.search(x).group(0))
# log.user_id = log.user_id.apply(lambda x: x[x.find("user_"):] if x.find('#error') < 0 else "")
log.user_id = log.user_id.apply(lambda x: x[x.find("user_"):])

# уберём начальную скобку из поля time.
# log.time = log.time.apply(lambda s: s[1:])
# log.time = log.time.apply(lambda s: s.replace('[', '') if type(s) == str else s)
log.time = log.time.apply(lambda s: s.replace('[', '', 1))

#print(log)
movies_db = pd.read_csv('movie_bd_v5.csv')
#print(movies_db[movies_db.budget == movies_db.budget.max()].original_title)
#print(movies_db.runtime.median())
movies_db['profit'] = movies_db.revenue - movies_db.budget
'''
movies_db['genres'] = movies_db.genres.str.split('|')
movies_db = movies_db.explode('genres')
movies_db['director'] = movies_db.director.str.split('|')
movies_db = movies_db.explode('director')
# m2008 = movies_db[(movies_db.release_year <= 2014) & (movies_db.release_year >= 2012)]
print(movies_db[movies_db.genres == 'Action'].groupby('director').genres.count().sort_values())
'''

#budget_value = movies_db.budget.mean() #movies_db.budget.value_counts(bins=2).index[1].left
# movies_db['cast'] = movies_db.cast.str.split('|')
# movies_db = movies_db.explode('cast')
#movies_db['genres'] = movies_db.genres.str.split('|')
#movies_db = movies_db.explode('genres')
#print(movies_db.groupby('genres')['original_title'].count().sort_values(ascending=False))


def get_time_year(n):
    n = int(n)
    if n < 3:
        return 'winter'
    if n < 6:
        return 'spring'
    if n < 9:
        return 'summer'
    if n < 12:
        return 'autumn'
    return 'winter'


#value = movies_db['vote_average'].value_counts(normalize=True).sort_index()
#print(value)
'''
movies_db['production_companies'] = movies_db.production_companies.str.split('|')
movies_db = movies_db.explode('production_companies')
movies_db['word_count'] = movies_db.overview.str.count(' ')
print(movies_db.groupby('production_companies')['word_count'].mean().sort_values(ascending=False))
'''

ids = movies_db['vote_average'].sort_values().tail(int(movies_db.size*0.1))
print(ids)

