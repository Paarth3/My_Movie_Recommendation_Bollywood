import pandas as pd
from ast import literal_eval
import statistics

df = pd.read_csv('IMDB_Movies_India.csv', encoding='ISO-8859-1')
df.drop(columns=['Year', 'Duration'], inplace=True)
df.dropna(inplace=True)
df.columns = ['Title', 'Genres', 'vote_average', 'vote_count', 'Director', 'Actor 1', 'Actor 2', 'Actor 3']

df_count_list = df['vote_count'].values.tolist()
new_count_list = []
for i in df_count_list:
    text = i.split(',')
    new_text = ''.join(text)
    new_count_list.append(int(new_text))

df['vote_count'] = new_count_list

weighted_rating = []
V = df['vote_count'].values.tolist()
R = df['vote_average'].values.tolist()
C = statistics.mean(R)
M = df['vote_count'].quantile(0.9)

for i in range(len(V)):
    weighted_rating.append((V[i]/(V[i] + M))*R[i] + (M/(V[i] + M))*C)

df_director_list = df['Director'].values.tolist()
new_director_list = []
for i in df_director_list:
    new_director_list.append([i])

df_actor1_list = df['Actor 1'].values.tolist()
df_actor2_list = df['Actor 2'].values.tolist()
df_actor3_list = df['Actor 3'].values.tolist()
new_cast_list = []
for i in range(len(df_actor1_list)):
    new_cast_list.append([df_actor1_list[i], df_actor2_list[i], df_actor3_list[i]])


my_df = pd.DataFrame()
my_df['Title'] = df['Title']
my_df['Weighted_Rating'] = weighted_rating
my_df['Director(s)'] = new_director_list
my_df['Cast'] = new_cast_list
my_df['Genres'] = [[i] for i in df['Genres'].values.tolist()]

my_df.sort_values(by=['Weighted_Rating'], inplace=True, ascending=False)
my_df.insert(loc=0, column='Movie_ID', value=range(len(my_df.index)))

my_df.to_csv('My_Movie_Data_Bollywood.csv', encoding='utf-8', index=False)