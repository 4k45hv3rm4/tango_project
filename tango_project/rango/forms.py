from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib. auth.models import User


class CategoryForm(forms.ModelForm):
    name  = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control  ', 'placeholder':'Type Category Name here... '}), max_length=128, )
    views = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control ','placeholder':''}))
    likes = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control '}))
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)


    class Meta:
        model = Category
        fields = ('name','views','likes' )


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,widget=forms.TextInput(attrs={'placeholder':'Please enter the title of the page Here....','class':'form-control  '}))
    url = forms.URLField(max_length=200, widget=forms.TextInput(attrs={'placeholder':'Please enter the URL of the page Here....','class':'form-control  '}))
    views = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Please enter the views of the page Here....','class':'form-control  '}))

    class Meta:
        model = Page

        exclude = ('category',)


    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
            return cleaned_data




class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in (self.fields['username'],self.fields['password'],self.fields['email']):
            field.widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = User
        fields=('username','email','password')




class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['website'].widget.attrs.update({'class': 'form-control'})
        self.fields['picture'].widget.attrs.update({'class': 'form-control-file'})


    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

