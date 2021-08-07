"""Posts Views"""

# Django
import numpy as np
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm2,PostForm, PostForm3
from .textToImageAPI.textToImage import textToImage
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .APIs.api import objDetect, get_text
# from django.http import HttpResponse
import json
from django.db.models import Count


# Models
from posts.models import Post, Like
from users.models import Profile, Follow

@login_required
def CreatePostView(request):
    if request.method=="POST":
        form = PostForm2(request.POST)
        if form.is_valid():
            profilePK = str(request.user.profile.pk)
            literature = form.cleaned_data['literature']
            final_dest = textToImage([literature],profilePK)
            ProfileObj = Profile.objects.get(pk=int(profilePK))
            PostObj = Post(profile=ProfileObj, title="Literature Post", photo="posts/photos/"+final_dest)
            PostObj.save()
            return redirect('/')
    form = PostForm2()
    return render(request, "posts/new.html", {'form':form})

@login_required
def CreatePhotoView(request):
    if request.method=="POST":
        form = PostForm3(request.POST, request.FILES)
        if form.is_valid():
            profilePK = str(request.user.profile.pk)
            caption = form.cleaned_data['caption']
            photo = form.cleaned_data['photo']
            choice = form.cleaned_data['choice']
            fs = FileSystemStorage()
            filename = fs.save("posts/photos/"+photo.name, photo)
            
            # Obj Detect
            if choice == "Object Detection":
                objDetect(filename)
            elif choice == "Extract text":
                text = get_text(filename)
                filename = "posts/photos/"+ textToImage([text],profilePK)    

            ProfileObj = Profile.objects.get(pk=int(profilePK))
            PostObj = Post(profile=ProfileObj, title=caption, photo=filename)
            PostObj.save()
            return redirect('/')
    form = PostForm3()
    return render(request, "posts/newphoto.html", {'form':form})


class PostFeedView(ListView):
    """Return all published posts."""
    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 4
    context_object_name = 'posts'

    def get_queryset(self):
        view = self.request.GET.get('view', 'personal')

        if view == 'global':
            return Post.objects.all().annotate(num_likes=Count('like')).order_by('-num_likes')
        else:
            print("Current user: ", self.request.user.username)
            followers_list = Follow.objects.filter(follower = self.request.user.profile).values("following")
            # print("focus here --> ", followers_list)
            new_context = Post.objects.filter(profile__in = followers_list).order_by("-created")
            return new_context
            
    def get_context_data(self, **kwargs):
        context = super(PostFeedView, self).get_context_data(**kwargs)
        context["view"] = self.request.GET.get('view', 'personal')
        return context

class PostDetailView(DetailView):
    """Detail view posts"""
    template_name = 'posts/detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'post_id'
    queryset = Post.objects.all()
    context_object_name = 'post'

@login_required
@require_POST
@csrf_exempt
def toggle_like(request):
    if request.method == 'POST':
        user = Profile.objects.get(user=request.user)
        post_id = request.POST["post_id"]
        print("post_id: ", post_id)
        post = Post.objects.get(pk=post_id)
        # toggle like/unlike
        try:
            Like.objects.get(user=user, post=post).delete()
            return JsonResponse({"like_status" : 0, "likes_cnt": str(post.like_set.all().count())})
        except Like.DoesNotExist:
            Like.objects.create(user=user, post=post)
            return JsonResponse({"like_status" : 1, "likes_cnt": str(post.like_set.all().count())})

    else:
        return HttpResponse("Failure :(") 

def autocompleteModel(request):
    search_qs = Profile.objects.filter(user__username__startswith=request.GET['search'])
    print(search_qs)
    results = []
    for r in search_qs:
        results.append(r.user.username)
        # print("Focus here --> ", r, type(r), type(r.user.username))
    resp = request.GET['callback'] + '(' + json.dumps(results) + ');'
    return HttpResponse(resp, content_type='application/json')