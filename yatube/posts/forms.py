from .models import Post, Group, Comment
from django import forms

group_list = Group.objects.all()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 7}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_text(self):
        data = self.cleaned_data['text']

        if data == '':
            raise forms.ValidationError('input field blyat dolboeb')
        return data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }
    
    def clean_text(self):
        data = self.cleaned_data['text']

        if data == '':
            raise forms.ValidationError('input some words dolboeb')
        return data
    # def clean_group(self):
    #     data = self.cleaned_data['group']

    #     if data not in group_list and data != '---------':
    #         raise forms.ValidationError('group not FOUND BLYAT')
    #     return data