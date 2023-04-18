from django.urls import path
from . import views


urlpatterns = [
    path('',views.HomePageView.as_view(),name='home-page'),
    path('posts',views.IndexPageView.as_view(),name='posts-index-page'),
    path('posts/<slug:slug>',views.ShowPageView.as_view(),name='post-show-page'),
    path('read-later',views.ReadLaterView.as_view(),name='read-later')
]
