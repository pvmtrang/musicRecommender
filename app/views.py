from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from .models import *
from .mlmodel import *
import os

from scipy.spatial.distance import cdist

import pickle
import numpy as np 
import pandas as pd 
from django.shortcuts import render

# def sample_detail(request, sample_id):
#     song_name_list = Song_Sample.objects.filter(sample_id = sample_id)
#     year_list = []
#     context = {
#         'song_list': song_name_list,
#         'year_list': year_list
#     }
#     return render(request, 'index.html', context)

# trong mlmodels da load data roi
# data = pd.read_csv("/home/tieu/Documents/musicRecommender/app/data-1M.csv")
# data = pd.DataFrame.from_records(Song.objects.all())


def recommendation_detail(request, sample_id):
    # hinh nhu ko can cai nay??
    # recommender = pickle.load(open('mlmodel.sav','rb'))
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
    sample_list = Sample.objects.all()
    context = {
        'recommend_list': rec_songs['name'],
        'song_list': song_list,
        'sample_list': sample_list
    }

    # return render(request, 'index.html', {'recommend_list':rec_songs[metadata_cols].to_dict(orient='records')})
    return render(request, 'index.html', context)
    