from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#Post
class Post(models.Model):
    body = models.TextField()
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True, max_length=1000)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

#Comment
class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

#Profile
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Restaurateur', 'restaurateur'),
        ('Amateur chef', 'amateur chef'),
    )

    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/defaultProfile.jpg', blank=True, max_length=1000)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


#Single item  
class SingleItem(models.Model):
    NAME_CHOICES = (
        ('Meat or Fish','meat or fish'),
        ('Frozen goods','frozen goods'),
        ('Canned food','canned food'),
        ('Fruits','fruits'),
        ('Vegetables','vegetables'),
        ('Dairy', 'dairy'),
        ('Nuts','nuts'),
        ('Eggs','eggs'),
        ('Pasta','pasta'),
        ('Bread','bread'),
        ('Salty snacks','salty snacks'),
        ('Sweet snacks','sweet snacks'),
        ('Pastry','pastry'),
        ('Water or Soft drinks','water or soft drinks'),
        ('Energy drinks','energy drinks'),
        ('Alcoholic drinks','alcoholic drinks'),
        ('Coffee or Tea','coffee or tea'),
        ('Spices','spices'),
        ('Seasoning','seasoning'),
    )
    STORAGE_CHOICES = (
            ('Pantry', 'pantry'),
            ('Fridge', 'fridge'),
            ('Freezer', 'freezer'),
            ('Other', 'other'),
        )

    item_name = models.CharField(max_length=50, blank=True)
    food_category = models.CharField(max_length=50, choices=NAME_CHOICES, blank=True, null=True)
    storage_method = models.CharField(max_length=30, choices=STORAGE_CHOICES, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)


#Grocery list
class GroceryList(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True, default='grocery list')
    list_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, to_field='username')
    grocery_items = models.ManyToManyField(SingleItem, blank=True, related_name='grocery_items')

    def save(self, *args, **kwargs):
        if not self.list_owner:
            self.list_owner = User.objects.get(username='default')
        super().save(*args, **kwargs)
