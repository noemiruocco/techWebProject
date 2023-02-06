from django.urls import path 
from .views import PostListView, PostCreateView, PostDetailView, PostEditView, PostDeleteView, CommentDeleteView
from .views import ProfileView, ProfileEditView, AddFollower, RemoveFollower, AddLike, AddDislike, FollowerList
from .views import UserSearch, SingleItemView, GroceryListView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/<int:pk>/followers/', FollowerList.as_view(), name='follower-list'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),
    path('search/', UserSearch.as_view(), name='profile-search'),
    path('grocery_list/', GroceryListView.as_view(), name='grocery-list'),
    path('add_item/', SingleItemView.as_view(), name='add-item'),
   
]