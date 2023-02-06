from django import forms
from .models import Post, Comment, SingleItem, GroceryList

# Post form
class PostForm(forms.ModelForm):
    body = forms.CharField(
        label = '',
        widget = forms.Textarea(attrs = {
            'rows' : '3',
            'placeholder' : 'Write something ...'
        })
    ) 

    images = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['body', 'image']


#Comment form 
class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label = '',
        widget = forms.Textarea(attrs = {
            'rows' : '3',
            'placeholder' : 'Write something ...'
        })
    ) 

    class Meta:
        model = Comment
        fields = ['comment']


#Single possible grocery list item form 
class SingleItemForm(forms.ModelForm):
    class Meta:
        model = SingleItem
        fields = ['item_name', 'food_category', 'storage_method', 'expiration_date']


#Grocery list form 
class GroceryListForm(forms.ModelForm):
    grocery_items = forms.ModelMultipleChoiceField(queryset=SingleItem.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = GroceryList
        fields = ['name', 'list_owner', 'grocery_items']