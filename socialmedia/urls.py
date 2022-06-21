from . import views
from django.urls import path


app_name = 'socialmedia'
urlpatterns = [
    path('', views.index, name='Home'),
    path('signin', views.signin, name='Signin'),
    path('signout', views.signout, name='Signout'),
    path('signup', views.signup, name='Signup'),
    path('profile', views.get_profile, name='GetProfile'),
    path('profile/<int:id>', views.get_profile_by_id, name='GetProfileById'),
    path('update_profile', views.update_profile, name='UpdateProfile'),
    path('make_post', views.make_post, name='MakePost'),
    path('like_post/<uuid:id>', views.like_post, name='LikePost'),
    path('handle_followers/<int:logedin_user_id>/<int:follower_id>', views.handle_followers, name="HandleFollowers"),
    path('search_user', views.do_search, name="SearchUser"),
    path('search_suggestions/<str:search_text>', views.search_suggestions, name='SearchSuggestions'),
    path('refresh_suggestions', views.refresh_suggestions, name="RefreshSuggestions"),
    path('make_comment', views.make_comment, name="MakeComment"),
    path('fetch_comments/<uuid:id>', views.fetch_comment, name='FetchComment'),
    path('explore', views.explore, name='Explore')
]
