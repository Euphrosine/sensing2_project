from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns =[
    path('accounts/login/',auth_views.LoginView.as_view(template_name='health_app/login.html'),name='login'),
    path('', views.display_chart_data, name='display_chart_data'),
    path('api/', views.chart_data_view, name='chart_data_view'),
    path('chart-data/', views.chart_view, name='chart_data'),
    path('logout/',auth_views.LogoutView.as_view(template_name='health_app/logout.html'),name='logout'),

]