#Run this in terminal: 
# pip3 install spotipy --upgrade

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import numpy as np
import pandas as pd
import pickle

from .models import Song
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import euclidean_distances
from scipy.spatial.distance import cdist
from collections import defaultdict

import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv("/home/tieu/Documents/musicRecommender/app/data.csv")
# data = pd.DataFrame.from_records(Song.objects.all())
data['unique'] = data['name'] + data['artists']
data = data.drop_duplicates(subset='unique', keep='first')

client_id = "a8ef1499b1f3468d9ce3186629adae0c"
client_secret = "30423bf1520b4e00a5bc4e076fe870aa"

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def find_song(name):
    song_data = defaultdict()
    results = sp.search(q= 'track: {}'.format(name), limit=1)
    if results['tracks']['items'] == []:
        return None

    results = results['tracks']['items'][0]
    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]

    song_data['name'] = [name]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]
    # Cha le spotify api ko tra ve 
    # cac feature explicit duration cac thu ben tren a??
    for key, value in audio_features.items():
        song_data[key] = value

    return pd.DataFrame(song_data)

#cluster songs with kmean

song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
                                  ('kmeans', KMeans(n_clusters=20, 
                                   verbose=False))
                                 ], verbose=False)
model = song_cluster_pipeline

# X = data.select_dtypes(np.number)

number_cols = ['valence', 'year', 'acousticness', 'danceability', 
    'duration_ms', 'energy', 'explicit',
    'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 
    'popularity', 'speechiness', 'tempo']

X = data[number_cols]

number_cols = list(X.columns)
# song_cluster_pipeline.fit(X)
model.fit(X)
song_cluster_labels = model.predict(X)
data['cluster_label'] = song_cluster_labels

def get_song_data(song, spotify_data):
    
    try:
        song_data = spotify_data[(spotify_data['name'] == str(song)) 
                                ].iloc[0]
        return song_data
    
    except IndexError:
        return find_song(str(song))
        
# Trong cai song_list nay chi co ten thoi
def get_mean_vector(song_list, spotify_data):
    
    song_vectors = []
    
    for song in song_list:
        song_data = get_song_data(song, spotify_data)
        if song_data is None:
            print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
            continue
        song_vector = song_data[number_cols].values
        song_vectors.append(song_vector)  
    
    song_matrix = np.array(list(song_vectors))
    return np.mean(song_matrix, axis=0)

# tu ({name, year}, {n, y}) -> {name:...}, {year:...}
def flatten_dict_list(dict_list):

    flattened_dict = defaultdict()
    for key in dict_list[0].keys():
        flattened_dict[key] = []
    
    for dictionary in dict_list:
        for key, value in dictionary.items():
            flattened_dict[key].append(value)
            
    return flattened_dict

# pickle.dump(model, open('mlmodel.sav','wb'))

# def recommend_songs( song_list, spotify_data, n_songs=10):
    
#     metadata_cols = ['name', 'year', 'artists']
#     song_dict = flatten_dict_list(song_list)
    
#     song_center = get_mean_vector(song_list, spotify_data)
#     scaler = song_cluster_pipeline.steps[0][1]
#     scaled_data = scaler.transform(spotify_data[number_cols])
#     scaled_song_center = scaler.transform(song_center.reshape(1, -1))
#     distances = cdist(scaled_song_center, scaled_data, 'cosine')
#     index = list(np.argsort(distances)[:, :n_songs][0])
    
#     rec_songs = spotify_data.iloc[index]
#     rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
#     return rec_songs[metadata_cols].to_dict(orient='records')