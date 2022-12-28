from django.urls import path
from . import views

urlpatterns = [
  path('', views.RealtorListView.as_view()),
  path('topseller', views.TopSellerView.as_view()),
  path('<str:pk>', views.RealtorView.as_view()),
]