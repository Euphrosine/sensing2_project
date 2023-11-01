from django.urls import path
from . import views


urlpatterns ={
     path('', views.display_chart_data, name='display_chart_data'),
    path('api/', views.chart_data_view, name='chart_data_view'),
    path('add-temp/', views.add_temp, name="add_temperature"),
}