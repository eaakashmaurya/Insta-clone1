"""Posts URLs"""

# Django
from django.urls import path
from django.contrib.auth.decorators import login_required

# Views
from posts import views


urlpatterns = [
    path(
        route='',
        view=login_required(views.PostFeedView.as_view()),
        name='feed'
    ),

    path(
        route='posts/newText',
        view=views.CreatePostView,
        name='create_post'
    ),

    path(
        route='posts/newPhoto',
        view=views.CreatePhotoView,
        name='create_photo'
    ),

    path(
        route='posts/<int:post_id>/',
        view=login_required(views.PostDetailView.as_view()),
        name='detail'
    ),

    path(
        route = 'like',
        view = views.toggle_like,
        name='like'
    ),

    path('search.json', views.autocompleteModel, name="autocomplete"),

]
