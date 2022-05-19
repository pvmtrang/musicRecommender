# #Run this in terminal: 
# # pip3 install spotipy --upgrade

# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# import os
# import numpy as np
# import pandas as pd
# import pickle

# from sklearn.cluster import KMeans
# from sklearn.preprocessing import StandardScaler
# from sklearn.pipeline import Pipeline
# from sklearn.metrics import euclidean_distances
# from scipy.spatial.distance import cdist
# from collections import defaultdict

# import warnings
# warnings.filterwarnings("ignore")

# class Recommender:
#     def __init__(self) -> None:
#         self.data = pd.read_csv("data-edited.csv")

#         client_id = "a8ef1499b1f3468d9ce3186629adae0c"
#         client_secret = "30423bf1520b4e00a5bc4e076fe870aa"

#         client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
#         self.sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
#         self.number_cols = ['valence', 'year', 'acousticness', 'danceability', 
#         'duration_ms', 'energy', 'explicit',
#         'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 
#         'popularity', 'speechiness', 'tempo']

#     def find_song(self, name, year):
#         song_data = defaultdict()
#         results = self.sp.search(q= 'track: {} year: {}'.format(name,year), limit=1)
#         if results['tracks']['items'] == []:
#             return None

#         results = results['tracks']['items'][0]
#         track_id = results['id']
#         audio_features = self.sp.audio_features(track_id)[0]

#         song_data['name'] = [name]
#         song_data['year'] = [year]
#         song_data['explicit'] = [int(results['explicit'])]
#         song_data['duration_ms'] = [results['duration_ms']]
#         song_data['popularity'] = [results['popularity']]

#         for key, value in audio_features.items():
#             song_data[key] = value

#         return pd.DataFrame(song_data)

# # print(find_song("Make you feel my love", 2008))

# # def find_song(name):
# #     song_data = defaultdict()
# #     song_data = Data
# #     results = sp.search(q= 'track: {}'.format(name), limit=5)
# #     if results['tracks']['items'] == []:
# #         return None

# #     for i in results:


# #     results = results['tracks']['items'][0]
# #     track_id = results['id']
# #     audio_features = sp.audio_features(track_id)[0]

# #     song_data['name'] = [name]
# #     song_data['year'] = [year]
# #     song_data['explicit'] = [int(results['explicit'])]
# #     song_data['duration_ms'] = [results['duration_ms']]
# #     song_data['popularity'] = [results['popularity']]

# #     for key, value in audio_features.items():
# #         song_data[key] = value

# #     return pd.DataFrame(song_data)

# #cluster songs with kmean
#     def cluster_song(self):
#         song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
#                                         ('kmeans', KMeans(n_clusters=20, 
#                                         verbose=False))
#                                         ], verbose=False)
#         self.model = song_cluster_pipeline

#         X = self.data.select_dtypes(np.number)
#         number_cols = list(X.columns)
#         # song_cluster_pipeline.fit(X)
#         self.model.fit(X)
#         # song_cluster_labels = song_cluster_pipeline.predict(X)
#         song_cluster_labels = self.model.predict(X)
#         self.data['cluster_label'] = song_cluster_labels



#     def get_song_data(self, song, spotify_data): 
#         try:
#             song_data = spotify_data[(spotify_data['name'] == song['name']) 
#                                     & (spotify_data['year'] == song['year'])].iloc[0]
#             return song_data
        
#         except IndexError:
#             return self.find_song(song['name'], song['year'])
        

#     def get_mean_vector(self, song_list, spotify_data):
        
#         song_vectors = []
        
#         for song in song_list:
#             song_data = self.get_song_data(song, spotify_data)
#             if song_data is None:
#                 print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
#                 continue
#             song_vector = song_data[self.number_cols].values
#             song_vectors.append(song_vector)  
        
#         song_matrix = np.array(list(song_vectors))
#         return np.mean(song_matrix, axis=0)


#     def flatten_dict_list(self, dict_list):
        
#         flattened_dict = defaultdict()
#         for key in dict_list[0].keys():
#             flattened_dict[key] = []
        
#         for dictionary in dict_list:
#             for key, value in dictionary.items():
#                 flattened_dict[key].append(value)
                
#         return flattened_dict

# # with open('model_pkl', 'wb') as files:
# #     pickle.dump(model, files)

#     def recommend_songs(self, song_list, n_songs=10):
#         spotify_data = self.data
#         metadata_cols = ['name', 'year', 'artists']
#         song_dict = self.flatten_dict_list(song_list)
        
#         song_center = self.get_mean_vector(song_list, spotify_data)
#         scaler = self.song_cluster_pipeline.steps[0][1]
#         scaled_data = scaler.transform(spotify_data[self.number_cols])
#         scaled_song_center = scaler.transform(song_center.reshape(1, -1))
#         distances = cdist(scaled_song_center, scaled_data, 'cosine')
#         index = list(np.argsort(distances)[:, :n_songs][0])
        
#         rec_songs = spotify_data.iloc[index]
#         rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
#         return rec_songs[metadata_cols].to_dict(orient='records')