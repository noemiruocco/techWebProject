from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, Comment, UserProfile, SingleItem, GroceryList
from .forms import PostForm, CommentForm, SingleItemForm, GroceryListForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, DeleteView

#Create a post 
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'socialPage/post_create.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


#Feed 
class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs): 
        logged_in_user = request.user 
        post = Post.objects.filter(
            author__profile__followers__in = [logged_in_user.id]
        ).order_by('-created_on')
        form = PostForm()

        context = {
            'post_list' : post,
            'form' : form,
        }

        return render(request, 'socialPage/post_list.html', context)

    def post(self, request, *args, **kwargs): 
        logged_in_user = request.user 
        post = Post.objects.filter(
            author__profile__followers__in = [logged_in_user.id]
        ).order_by('-created_on')
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list' : post,
            'form' : form,
        }
        return render(request, 'socialPage/post_list.html', context)


#Detailed post with related comments 
class PostDetailView(LoginRequiredMixin, View):
     def get(self, request, pk, *args, **kwargs):  
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post' : post,
            'form' : form,
            'comments' : comments,
        }

        return render(request, 'socialPage/post_detail.html', context)

    # For adding a comment 
     def post(self, request, pk, *args, **kwargs): 
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post' : post,
            'form' : form,
            'comments' : comments 
        }

        return render(request, 'socialPage/post_detail.html', context)


#Post edit and delete 
class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'socialPage/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk' : pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'socialPage/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


#Delete a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'socialPage/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk' : pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


#Profile 
class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)

        context = {
            'user' : user,
            'profile' : profile,
            'posts' : posts,  
            'number_of_followers' : number_of_followers,
            'is_following' : is_following,
        }

        return render(request, 'socialPage/profile.html', context)


#Profile edit
class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name','bio','role','birth_date','location','picture']
    template_name = 'socialPage/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


#Adding and removing a follower 
class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect('profile', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('profile', pk=profile.pk)


#Like and dislike 
class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False 

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False 

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)
        
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False 

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False 

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add (request.user)

        if is_dislike:
            post.dislikes.remove(request.user)
        
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


#Searching user 
class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains = query )
        )

        context = {
            'profile_list': profile_list,
        }

        return render(request, 'socialPage/search.html', context)


#Followers list on a profile
class FollowerList(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()

        context = {
            'profile' : profile,
            'followers' : followers, 
        }

        return render(request, 'socialPage/follower_list.html', context)


#Single items view
class SingleItemView(View):
    def get(self, request, *args, **kwargs):
        name = SingleItem.item_name
        category = SingleItem.food_category
        default_storage = SingleItem.storage_method
        default_expiration = SingleItem.expiration_date
        items = SingleItem.objects.all().order_by('item_name')

        context = {
            'name' : name,
            'category' : category,
            'default storage' : default_storage,
            'default expiration' : default_expiration,
            'items' : items,
        }

        return render(request, 'socialPage/add_item.html', context)


#Grocery list view
class GroceryListView(View):
    def get(self, request, *args, **kwargs):
        grocery_list = GroceryList.objects.get(list_owner=request.user)
        grocery_items = grocery_list.grocery_items.all()

        context = {
            'grocery_list': grocery_list,
            'grocery_items': grocery_items,
        }

        return render(request, 'socialPage/grocery_list.html', context)


