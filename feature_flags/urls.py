from django.urls import path
from . import views

urlpatterns = [
   

    path('subscribe-user/', views.subscribe_user),
    path('create-feature/', views.create_feature),
    path('add-user-override/', views.add_user_override),
    path('add-group-override/', views.add_group_override),
    path('add-region-override/', views.add_region_override),
    path('check-feature/', views.check_feature),

    path('users/', views.list_users),
    path('features/', views.list_features),
    path('user-overrides/', views.list_user_overrides),
    path('group-overrides/', views.list_group_overrides),
    path('region-overrides/', views.list_region_overrides),
    path("dashboard/", views.dashboard),
    path("create-user/", views.create_user),
    path("subscribe-user-ui/", views.subscribe_user_ui),
    path('login-user/', views.login_view),


   
   
]
