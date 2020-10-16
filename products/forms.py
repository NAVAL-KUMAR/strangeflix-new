from django import forms



class CommentForm(forms.Form):
    text = forms.CharField(label='Add Comment :', max_length=300)
    
class NewVideoForm(forms.Form):
    title = forms.CharField(label='Title', max_length=20)
    description = forms.CharField(label='Description', max_length=300)
    file = forms.FileField(label='Add Video')
    fileI = forms.FileField(label='Add Image Thumbnail')
