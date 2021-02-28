import pandas as pd
import numpy as np

all_films = pd.read_csv('movie_bd_v5.csv')
# 0. Preparing.
## Get columns name
columns = all_films.columns
''' ['imdb_id', 'budget', 'revenue', 'original_title', 'cast', 'director',
       'tagline', 'overview', 'runtime', 'genres', 'production_companies',
       'release_date', 'vote_average', 'release_year']
'''
## New column for title + imdb
all_films['title_imdb'] = all_films.original_title + ' (' + all_films.imdb_id + ')'

## New column with profit
all_films['profit'] = all_films.revenue - all_films.budget
## New column for release_month
all_films['release_month'] = list(map(int, all_films.release_date.str.split('/').str[0]))

## Split genres
all_films['genres'] = all_films.genres.str.split('|')
## Split directors
all_films['director'] = all_films.director.str.split('|')
## Split cast
all_films['cast'] = all_films.cast.str.split('|')
## Split production_companies
all_films['production_companies'] = all_films.production_companies.str.split('|')


## Function fo get season by number month as string
def get_season(n):
    """ Function to define season by month number """
    seasons = ['winter', 'spring', 'summer', 'autumn']
    season_number = (n // 3) % 4
    return seasons[season_number]


# Вопрос 1. У какого фильма из списка самый большой бюджет?
def task_1(ans):
    """ Get films by list and get title and imdb of film with maximal budget """
    films = all_films[all_films.title_imdb.isin(ans)].query('budget == budget.max()')
    return films.title_imdb.item()


# Вопрос 2. Какой из фильмов самый длительный (в минутах)?
def task_2(ans):
    """ Get films by list with maximal budget """
    films = all_films[all_films.title_imdb.isin(ans)].query('runtime == runtime.max()')
    return films.title_imdb.item()


# Вопрос 3. Какой из фильмов самый короткий (в минутах)?
def task_3(ans):
    films = all_films[all_films.title_imdb.isin(ans)].query('runtime == runtime.min()')
    '''print title and imdb of film with maximal budget'''
    return films.title_imdb.item()


# Вопрос 4. Какова средняя длительность фильмов?
def task_4(ans):
    """ Get average value of runtime """
    return round(all_films.runtime.mean())


# Вопрос 5. Каково медианное значение длительности фильмов?
def task_5(ans):
    """ Get median value of runtime """
    return round(all_films.runtime.median())


# Вопрос 6. Какой фильм самый прибыльный?
def task_6(ans):
    """ Get film with maximal profit. """
    films = all_films[all_films.title_imdb.isin(ans)].query('profit == profit.max()')
    return films.title_imdb.item()


# Вопрос 7. Какой фильм самый убыточный?
def task_7(ans):
    """ Get film with minimal profit"""
    '''Get films by list'''
    films = all_films[all_films.title_imdb.isin(ans)]
    ''' Return title and imdb of film with maximal profit'''
    return films[films.profit == films.profit.min()].title_imdb.item()


# Вопрос 8. У скольких фильмов из датасета объем сборов оказался выше бюджета?
def task_8(ans):
    """ Count of films with revenue > budget (positive profit)"""
    return len(all_films[all_films.profit > 0])


# Вопрос 9. Какой фильм оказался самым кассовым в 2008 году?
def task_9(ans):
    """ Get film with maximal revenue at 2008 year"""
    films = all_films[all_films.title_imdb.isin(ans)]
    '''Get films from 2008 '''
    films2008 = films[films.release_year == 2008]
    ''' Return title and imdb of film with maximal revenue '''
    return films2008[films2008.revenue == films2008.revenue.max()].title_imdb.item()


# Вопрос 10. Самый убыточный фильм за период с 2012 по 2014 годы (включительно)?
def task_10(ans):
    """ Film with minimal profit (maximal negative value) by 2012-2014 """
    ''' Get films by list '''
    films = all_films[all_films.title_imdb.isin(ans)]
    '''Get films from 2012-2014'''
    films12_14 = films[films.release_year.isin(range(2012, 2014 + 1))]
    ''' print title and imdb of film with minimal profit from 2012 to 2014 years'''
    return films12_14[films12_14.profit == films12_14.profit.min()].title_imdb.item()


# Вопрос 11. Какого жанра фильмов больше всего?
def task_11(ans):
    """ Get genre with maximal films. """
    ''' explode and group all films by genres '''
    all_films_by_genres = all_films.explode('genres').query(f'genres.isin({ans})').groupby('genres')
    ''' Return popular genre '''
    return all_films_by_genres.size().sort_values(ascending=False).index[0]

    all_genres = set(np.concatenate(list(all_films.genres)))



# Вопрос 12. Фильмы какого жанра чаще всего становятся прибыльными?
def task_12(ans):
    """ Get most profit genre """
    all_films_by_genres = all_films[all_films.profit > 0].explode('genres') \
        .query(f'genres.isin({ans})') \
        .groupby('genres')
    ''' Return profit genre '''
    return all_films_by_genres.size().sort_values(ascending=False).index[0]


# Вопрос 13. У какого режиссёра самые большие суммарные кассовые сборы?
def task_13(ans):
    """ Get director with maximal summary of revenue """
    all_films_by_director = all_films.explode('director') \
        .query(f'director.isin({ans})') \
        .groupby('director') \
        .sum()
    ''' Return the director with maximal summary of revenue '''
    return all_films_by_director.revenue.sort_values(ascending=False).index[0]


# Вопрос 14. Какой режиссер снял больше всего фильмов в стиле Action?
def task_14(ans):
    all_films_genre = all_films.explode('genres')
    ''' explode and group all films by director'''
    all_films_genre_dir = all_films_genre.explode('director').query(f'director.isin({ans})')
    ''' First solution with filters and groups'''
    ''' get Action genre and group by director and calculate count '''
    all_films_dir_groups = all_films_genre_dir.query("genres == 'Action'").groupby('director').count()
    ''' Return the director with maximal unique imdb '''
    return all_films_dir_groups.imdb_id.sort_values(ascending=False).index[0]

    ''' Second solution with pivot table'''
    ''' Make table with genres and directors. Value = count of imdb_id'''
    pt = all_films_genre_dir.pivot_table(values='imdb_id', index='genres', columns='director', aggfunc='count',
                                         fill_value=0)
    return pt.loc['Action'].sort_values(ascending=False).index[0]


# Вопрос 15. Фильмы с каким актером принесли самые высокие кассовые сборы в 2012 году?
def task_15(ans):
    all_films_actor = all_films[all_films.release_year == 2012].explode('cast').query(f'cast.isin({ans})')
    ''' group by actor and calculate summary '''
    all_films_cast_groups = all_films_actor.groupby('cast').sum()
    ''' Print the actor with maximal revenue '''
    return all_films_cast_groups.revenue.sort_values(ascending=False).index[0]


# Вопрос 16. Какой актер снялся в большем количестве высокобюджетных фильмов?
# Примечание: в фильмах, где бюджет выше среднего по данной выборке.
def task_16(ans):
    """ Get actor with maximal count of high budget films """
    ''' Get films with budget more mean value '''
    all_profit_films = all_films.query('budget > budget.mean()')
    ''' Explode by actor and group films by actor fro task'''
    actors_films = all_profit_films.explode('cast').query(f'cast.isin({ans})')
    grouped_films = actors_films.groupby('cast').imdb_id.count()
    ''' Get actor from profit budget films '''
    return grouped_films.sort_values(ascending=False).index[0]


# Вопрос 17. В фильмах какого жанра больше всего снимался Nicolas Cage?
def task_17(ans):
    """ Get most popular genre for Nicolas Cage """
    ''' Get all films with Cage '''
    nicolas_films = all_films.explode('cast').query('cast == \'Nicolas Cage\'')
    ''' Explode films by genres '''
    nicolas_films_genres = nicolas_films.explode('genres')
    ''' Get genres from task and group by genres'''
    nicolas_genres = nicolas_films_genres[nicolas_films_genres.genres.isin(ans)].groupby('genres')
    ''' Return most popular genre'''
    return nicolas_genres.size().sort_values(ascending=False).index[0]

    ''' Solution by pivot table '''
    nicolas_pt = nicolas_films_genres.pivot_table(values='imdb_id', index='cast', columns='genres', aggfunc='count',
                                                  fill_value=0)
    nicolas_pt.loc['Nicolas Cage'].sort_values(ascending=False)
    return nicolas_pt.loc['Nicolas Cage'].sort_values(ascending=False).index[0]


# Вопрос 18. Самый убыточный фильм от Paramount Pictures?
def task_18(ans):
    """ Get Paramount Pictures films with minimal profit """
    paramout_films = all_films.explode('production_companies').query('production_companies == \'Paramount Pictures\'')
    ''' Filter task films '''
    paramout_films = paramout_films.query(f'title_imdb.isin({ans})')
    ''' Return title + imdb for film with minimal profit '''
    return paramout_films.query(f'profit == profit.min()').title_imdb.item()


# Вопрос 19. Какой год стал самым успешным по суммарным кассовым сборам?
def task_19(ans):
    """ Get year with maximal revenue """
    ''' Get films by task variants and group by years with calculate sum of values'''
    year_films = all_films[all_films.release_year.isin(ans)].groupby('release_year').sum()
    ''' Sort by revenue and return year with maximal revenue '''
    return year_films['revenue'].sort_values(ascending=False).index[0]


# Вопрос 20. Какой самый прибыльный год для студии Warner Bros?
def task_20(ans):
    """ Get year with maximal revenue for Warner Bros """
    ''' Get films by task variants'''
    # year_films = all_films[all_films.release_year.isin(ans)].copy()
    year_films = all_films.query(f'release_year.isin({ans})').copy()
    year_films['production_companies'] = year_films['production_companies'].str.join('|')

    ''' Get WB films and group by years with calculate summary values '''
    wb_films = year_films[year_films.production_companies.str.contains('Warner Bros')].groupby('release_year').sum()

    return wb_films['profit'].sort_values(ascending=False).index[0]


# Вопрос 21. В каком месяце за все годы суммарно вышло больше всего фильмов?
def task_21(ans):
    """ Get month with maximal films """
    months = [0, 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
              'Ноябрь', 'Декабрь']
    month_groups = all_films.groupby('release_month').size()
    return months[month_groups.sort_values(ascending=False).index[0]]


# Вопрос 22. Сколько суммарно вышло фильмов летом (за июнь, июль, август)?
def task_22(ans):
    """ Get films count by summer """
    return len(all_films[all_films.release_month.isin([6, 7, 8])])


# Вопрос 23. Для какого режиссера зима — самое продуктивное время года?
def task_23(ans):
    """ Get producer with maximal films by winter. """
    ''' Get winter_films and explode films by director '''
    winter_films = all_films.query('release_month.isin([1, 2, 12])').explode('director')
    ''' Filter films by directors from answer '''
    winter_films = winter_films[winter_films.director.isin(ans)]
    ''' Group by director and get size of groups '''
    director_groups = winter_films.groupby('director').size().sort_values(ascending=False)
    return director_groups.index[0]


# Вопрос 24. Какая студия даёт самые длинные названия своим фильмам по количеству символов?
def task_24(ans):
    """ Get studio with maximal average length of title """
    ''' Filter by studio from task '''
    studio_films = all_films.explode('production_companies').query(f'production_companies.isin({ans})')
    ''' New column for length of title '''
    studio_films['title_length'] = studio_films.original_title.str.len()
    ''' Group by companies name and sort by mean value of title length '''
    return studio_films.groupby('production_companies').title_length.mean().sort_values(ascending=False).index[0]


# Вопрос 25. Какая студия даёт самые длинные названия своим фильмам по количеству символов?
def task_25(ans):
    """ Get studio with maximal words count into overview """
    ''' Filter by studio from task '''
    studio_films = all_films.explode('production_companies').query(f'production_companies.isin({ans})')
    ''' New column for length of title '''
    studio_films['overview_length'] = studio_films.overview.str.count(' ')
    ''' Group by companies name and sort by mean value of title length '''
    return studio_films.groupby('production_companies').overview_length.mean().sort_values(ascending=False).index[0]


# Вопрос 26. Какие фильмы входят в один процент лучших по рейтингу?
def task_26(ans):
    """ What film list included in 1% best by vote """
    ''' Split answers to lists of films '''
    split_answers = list(map(lambda x: x.split(', '), ans))
    ''' Get 1% best films'''
    best_films = all_films.sort_values('vote_average', ascending=False).head(int(len(all_films) * 0.01))
    for i in range(len(split_answers)):
        if len(best_films.query(f'original_title.isin({split_answers[i]})')) == len(split_answers[i]):
            return ans[i]


# Вопрос 27. Какие актеры чаще всего снимаются в одном фильме вместе?
def task_27(ans):
    """ """
    ''' Split actors by pair'''
    split_answers = list(map(lambda x: list(map(lambda s: s.strip(), x.split('&'))), ans))
    ''' Get all actor from answers '''
    all_actors = list(np.concatenate(split_answers))
    ''' Get films with actors '''
    films = all_films.explode('cast').query(f'cast.isin({all_actors})')
    films['cast_group'] = films.cast \
        .apply(lambda cast: [i for i in range(len(split_answers)) if cast in split_answers[i]][0])
    ''' Get films with one of pair '''
    cast_films = films.groupby(['imdb_id', 'cast_group']).filter(lambda g: len(g) == 2)
    ''' Return title for most frequent pair '''
    return ans[cast_films.groupby('cast_group').size().sort_values(ascending=False).index[0]]


test = {
    '1': {
        'solver': task_1,
        'answers': ['The Dark Knight Rises (tt1345836)', 'Spider-Man 3 (tt0413300)',
                    'Avengers: Age of Ultron (tt2395427)',
                    'The Warrior\'s Way (tt1032751)', 'Pirates of the Caribbean: On Stranger Tides (tt1298650)']
    },
    '2': {
        'solver': task_2,
        'answers': ['The Lord of the Rings: The Return of the King (tt0167260)', 'Gods and Generals (tt0279111)',
                    'King Kong (tt0360717)', 'Pearl Harbor (tt0213149)', 'Alexander (tt0346491)']
    },
    '3': {
        'solver': task_3,
        'answers': ['Home on the Range (tt0299172)', 'The Jungle Book 2 (tt0283426)', 'Winnie the Pooh (tt1449283)',
                    'Corpse Bride (tt0121164)', 'Hoodwinked! (tt0443536)']
    },
    '4': {
        'solver': task_4,
        'answers': [115, 110, 105, 120, 100]
    },
    '5': {
        'solver': task_5,
        'answers': [107, 112, 101, 120, 115]
    },
    '6': {
        'solver': task_6,
        'answers': ['The Avengers (tt0848228)', 'Minions (tt2293640)', 'Star Wars: The Force Awakens (tt2488496)',
                    'Furious 7 (tt2820852)', 'Avatar (tt0499549)']
    },
    '7': {
        'solver': task_7,
        'answers': ['Supernova (tt0134983)', 'Frozen (tt2294629)', 'Flushed Away (tt0424095)',
                    'The Adventures of Pluto Nash (tt0180052)', 'The Lone Ranger (tt1210819)']
    },
    '8': {
        'solver': task_8,
        'answers': [1478, 1520, 1241, 1135, 1398]
    },
    '9': {
        'solver': task_9,
        'answers': ['Madagascar: Escape 2 Africa (tt0479952)', 'Iron Man (tt0371746)', 'Kung Fu Panda (tt0441773)',
                    'The Dark Knight (tt0468569)', 'Mamma Mia! (tt0795421)']
    },
    '10': {
        'solver': task_10,
        'answers': ['Winter\'s Tale (tt1837709)', 'Stolen (tt1656186)', 'Broken City (tt1235522)',
                    'Upside Down (tt1374992)', 'The Lone Ranger (tt1210819)']
    },
    '11': {
        'solver': task_11,
        'answers': ['Action', 'Adventure', 'Drama', 'Comedy', 'Thriller']
    },
    '12': {
        'solver': task_12,
        'answers': ['Drama', 'Comedy', 'Action', 'Thriller', 'Adventure']
    },
    '13': {
        'solver': task_13,
        'answers': ['Steven Spielberg', 'Christopher Nolan', 'David Yates', 'James Cameron', 'Peter Jackson']
    },
    '14': {
        'solver': task_14,
        'answers': ['Ridley Scott', 'Guy Ritchie', 'Robert Rodriguez', 'Quentin Tarantino', 'Tony Scott']
    },
    '15': {
        'solver': task_15,
        'answers': ['Nicolas Cage', 'Tom Hardy', 'Chris Hemsworth', 'Jim Sturgess', 'Emma Stone']
    },
    '16': {
        'solver': task_16,
        'answers': ['Tom Cruise', 'Mark Wahlberg', 'Matt Damon', 'Angelina Jolie', 'Adam Sandler']
    },
    '17': {
        'solver': task_17,
        'answers': ['Drama', 'Action', 'Thriller', 'Adventure', 'Crime']
    },
    '18': {
        'solver': task_18,
        'answers': ['K-19: The Widowmaker (tt0267626)', 'Next (tt0435705)', 'Twisted (tt0315297)',
                    'The Love Guru (tt0811138)', 'The Fighter (tt0964517)']
    },
    '19': {
        'solver': task_19,
        'answers': [2014, 2008, 2012, 2002, 2015]
    },
    '20': {
        'solver': task_20,
        'answers': [2014, 2008, 2012, 2010, 2015]
    },
    '21': {
        'solver': task_21,
        'answers': ['Январь', 'Июнь', 'Декабрь', 'Сентябрь', 'Май']
    },
    '22': {
        'solver': task_22,
        'answers': [345, 450, 478, 523, 381]
    },
    '23': {
        'solver': task_23,
        'answers': ['Steven Soderbergh', 'Christopher Nolan', 'Clint Eastwood', 'Ridley Scott', 'Peter Jackson']
    },
    '24': {
        'solver': task_24,
        'answers': ['Universal Pictures (Universal)', 'Warner Bros', 'Jim Henson Company, The', 'Paramount Pictures',
                    'Four By Two Productions']
    },
    '25': {
        'solver': task_25,
        'answers': ['Universal Pictures', 'Warner Bros', 'Midnight Picture Show', 'Paramount Pictures',
                    'Total Entertainment']
    },
    '26': {
        'solver': task_26,
        'answers': ['Inside Out, The Dark Knight, 12 Years a Slave',
                    'BloodRayne, The Adventures of Rocky & Bullwinkle',
                    'Batman Begins, The Lord of the Rings: The Return of the King, Upside Down',
                    '300, Lucky Number Slevin, Kill Bill: Vol. 1',
                    'Upside Down, Inside Out, Iron Man']
    },
    '27': {
        'solver': task_27,
        'answers': ['Johnny Depp & Helena Bonham Carter', 'Ben Stiller & Owen Wilson', 'Vin Diesel & Paul Walker',
                    'Adam Sandler & Kevin James', 'Daniel Radcliffe & Rupert Grint']
    }
}


def form_answer(answer, variants):
    num_answer = variants.index(answer)
    full_answer = str(num_answer + 1) + '. ' + str(variants[num_answer])
    print(full_answer)
    return full_answer


answers = {}

for number in test:
    print("#task" + number)
    answers[number] = form_answer(test[number]['solver'](test[number]['answers']), test[number]['answers'])

from itertools import combinations
print(list(combinations([1, 2, 3, 4, 5], 2)))

all_films.cast.