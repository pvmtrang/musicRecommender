from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from matplotlib.style import context
from .models import *
from .mlmodel import *
import os

from scipy.spatial.distance import cdist


import pickle
import numpy as np 
import pandas as pd 
from django.shortcuts import render
from django.contrib import messages 

def sample_detail(request, sample_id):
    song_name_list = Song_Sample.objects.filter(sample_id = sample_id)
    year_list = []
    # song_list = []
    # for i in song_name_list:
    #     song_list.append(Song.objects.filter(id = i.song_id))
    # print(song_list)
    # for i in song_list:
    #     year_list.append(i.get_year())
    # print(song_name_list)
    context = {
        'song_list': song_name_list,
        'year_list': year_list
    }
    return render(request, 'index.html', context)

data = pd.read_csv("/home/tieu/Documents/musicRecommender/app/data.csv")

def recommendation_detail(request, sample_id):
    recommender = pickle.load(open('/home/tieu/Documents/musicRecommender/app/mlmodel.sav','rb'))
    song_list = Song_Sample.objects.filter(sample_id = sample_id)
    n_songs = 10
    
    metadata_cols = ['name', 'year', 'artists']
    # song_dict = flatten_dict_list(song_list)
    
    song_center = get_mean_vector(song_list, data)
    scaler = model.steps[0][1]
    scaled_data = scaler.transform(data[number_cols])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))
    distances = cdist(scaled_song_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:, :n_songs][0])
    
    rec_songs = data.iloc[index]
    # rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
    rec_songs = rec_songs[~rec_songs['name'].isin(song_list)]

    # return render(request, 'index.html', {'recommend_list':rec_songs[metadata_cols].to_dict(orient='records')})
    return render(request, 'index.html', {'recommend_list':rec_songs['name']})
    