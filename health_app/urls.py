from django.urls import path
from . import views


urlpatterns ={
    path('', views.display_chart_data, name='display_chart_data'),
    path('api/', views.chart_data_view, name='chart_data_view'),
    path('chart-data/', views.chart_view, name='chart_data'),
   
}