import pandas as pd

tmdb_credits = pd.read_csv('tmdb_5000_credits.csv')
tmdb_movies = pd.read_csv('tmdb_5000_movies.csv')

#Normalization
"""list_cast = []
for cast in tmdb_credits.cast:
    list_cast.append(pd.DataFrame(eval(cast)))
tmdb_credits.cast = pd.Series(list_cast)
list_crew = []
for crew in tmdb_credits.crew:
    list_crew.append(pd.DataFrame(eval(crew)))
tmdb_credits.crew = pd.Series(list_crew)
"""
print('1.For each movie, compute the number of cast members')
number_cast_members = []
for cast in tmdb_credits.cast:
    number_cast_members.append((len(pd.DataFrame(eval(cast)))))
print(pd.Series(number_cast_members, index=tmdb_credits.title))

print('\n2.How many movies do not have a homepage?')
print(len(tmdb_movies.homepage) - tmdb_movies.homepage.count())

print('\n3.For each year, how many movies do not have a homepage?')
tmdb_movies['release_year'] = tmdb_movies.release_date.str[:4]
print(tmdb_movies.groupby('release_year').title.count() - tmdb_movies.groupby('release_year').homepage.count())

print('\n4.Extract the domain of each homepage.')
print(pd.Series(list(tmdb_movies.homepage.str.partition('//')[2].str.partition('/')[0]), index=tmdb_movies.title))

print('\n6.For each movie, compute the gross margin (difference between revenue and budget)')
print(pd.Series(list(tmdb_movies.revenue - tmdb_movies.budget), index=tmdb_movies.title))

print('\n7.For each movie, compute the number of crew members')
number_crew_members = []
for crew in tmdb_credits.crew:
    number_crew_members.append((len(pd.DataFrame(eval(crew)))))
print(pd.Series(number_crew_members, index=tmdb_credits.title))

print('\n8.For each movie, compute the number of directors')
number_general_directors = []
number_all_directors = []
for crew in tmdb_credits.crew:
    df = pd.DataFrame(eval(crew))
    if len(df) != 0:
        number_general_directors.append(len(df.loc[df.job.str.lower() == 'director']))
        number_all_directors.append(len(df.loc[df.job.str.lower().str.contains('director')]))
    else:
        number_general_directors.append(0)
        number_all_directors.append(0)
print(pd.DataFrame({'general_directors':pd.Series(number_general_directors, index=tmdb_movies.title), 'all_directors':pd.Series(number_all_directors, index=tmdb_movies.title)}))

print('\n9.For each language, compute the number of movies where such language is spoken')
number_movies_language = dict()
for list_language in tmdb_movies.spoken_languages:
    df = pd.DataFrame(eval(list_language))
    if len(df) != 0:
        for language in df.iso_639_1:
            number_movies_language[language] = number_movies_language.setdefault(language, 0) + 1
print(pd.Series(number_movies_language))

print('\n10.For each company and each decade, compute the overall revenue')
tmdb_movies['decade'] = tmdb_movies.release_date.str[:3] + '0'
grouped_decade = tmdb_movies.groupby('decade')
overall_revenue = dict()
for decade, group in grouped_decade:
    for index in group.index:
        companies = pd.DataFrame(eval(group.production_companies[index]))
        if len(companies) != 0:
            for company in companies.name:
                overall_revenue[(decade, company)] = overall_revenue.setdefault((decade, company), 0) + group.revenue[index] 
print(pd.Series(overall_revenue))

print('\n11.For each decade, compute the company with maximum revenue')
grouped_decade = pd.Series(overall_revenue).groupby(level=0).max()
for max_revenue in grouped_decade:
    for decade, company in overall_revenue:
        if overall_revenue[(decade, company)] == max_revenue:
            print(decade, company, max_revenue)
            
print('\n12.In each year, how many movies have revenue smaller than the budget')
tmdb_movies['release_year'] = tmdb_movies.release_date.str[:4]
print(tmdb_movies[tmdb_movies.revenue < tmdb_movies.budget].groupby('release_year').count().title)
