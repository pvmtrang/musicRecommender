from django.urls import path, re_path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('getdata/', views.get_data, name='get_data'),
    path('<int:sample_id>/',views.recommendation_detail),
    # path('<int:sample_id>/recommendation', , name='recommendation_detail')
]