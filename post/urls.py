from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('list', views.PostListView.as_view(), name='list'),
    path('detail/<slug:slug>', views.PostDetailView.as_view(), name='detail'),
    path('<slug:slug>/like', views.LikeView.as_view(), name='like'),
    path('contact-us', views.ContactUsView.as_view(), name='contact_us'),
]