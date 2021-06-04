from django.urls import path
from recipe import views
urlpatterns=[
    path('',views.recipe_list),
    path('detail/',views.recipe_detail),
    path('login/',views.login),
    path('logout/',views.logout),
    path('before/',views.detail_before)
]