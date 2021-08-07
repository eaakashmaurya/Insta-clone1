"""User views."""

# Django
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http.response import HttpResponse, JsonResponse

# Forms
from users.forms import SignupForm

# Models
from posts.models import Post, Like
from users.models import Profile, Follow

# Create your views here.


class SignupView(FormView):
    """Signup View."""
    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """If the form is valid save the user"""
        form.save()
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    """Login view"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout View."""

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update a user's profile view"""
    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']
    # Return success url
    def get_object(self):
        """Return user's profile"""
        return self.request.user.profile
    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username_slug': username})


class UserDetailView(DetailView):
    """User detail view."""
    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username_slug'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context"""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(profile__user=user).order_by('-created')

        # can be improved
        view_user = Profile.objects.filter(user_id = user.pk)[0]  # redundent query
        loggedin_user = Profile.objects.filter(user_id = self.request.user.pk)[0] #redundent query
        # print("view_user: ", type(view_user), type(user))
        context["user_follows_this"] = Follow.objects.all().filter(follower = loggedin_user, following = view_user) and True or False
        # print(type(context["user"]))
        # print(user)
        # print("Logged-in user: ", self.request.user, type(self.request.user))
        print("Follows? : ", context["user_follows_this"])

        return context

@login_required
@require_POST
@csrf_exempt
def toggle_follow(request):
    if request.method == 'POST':
        loggedin_user = Profile.objects.get(user=request.user)
        user_id = request.POST["user_id"]
        print("user_id: ", user_id)
        # return HttpResponse("Success!!")
        view_user = Profile.objects.get(pk=user_id)
        # toggle follow
        try:
            Follow.objects.get(follower=loggedin_user, following=view_user).delete()
            return JsonResponse({"follow_button_status" : "Follow", "followers_cnt" : str(view_user.following.all().count())})
        except Follow.DoesNotExist:
            Follow.objects.create(follower=loggedin_user, following=view_user)
            return JsonResponse({"follow_button_status" : "Following", "followers_cnt" : str(view_user.follower.all().count())})

    else:
        return HttpResponse("Failure :(")