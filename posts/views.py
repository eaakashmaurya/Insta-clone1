"""Posts Views"""

# Django
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

# Models
from posts.models import Post, Like
from users.models import Profile

# Forms
from posts.forms import PostForm


# LoginRequired into Views
class CreatePostView(LoginRequiredMixin, CreateView):
    """Create New Post View"""
    template_name = 'posts/new.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        """Add User and profile to context."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context


class PostFeedView(ListView):
    """Return all published posts."""
    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 4
    context_object_name = 'posts'


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
        # toggle like
        try:
            Like.objects.get(user=user, post=post).delete()
            return JsonResponse({"like_status" : 0, "likes_cnt": str(post.like_set.all().count())})
        except Like.DoesNotExist:
            Like.objects.create(user=user, post=post)
            return JsonResponse({"like_status" : 1, "likes_cnt": str(post.like_set.all().count())})

    else:
        return HttpResponse("Failure :(") 

    