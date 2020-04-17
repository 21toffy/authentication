from django import forms
from .models import *

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get("password2")
        if p1 and p2:
            if p1 != p2:
                raise ValidationError('passwords do not match lol')
        return self.cleaned_data

    def clean_email(self):
        email= self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise ValidationError('damn it this email already exists ')
        return email

    def clean_username(self):
        username= self.cleaned_data['username']
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise ValidationError('damn it this username already exists ')
        return username 


    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password','password2']
        





class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['Avi','linkedin', 'twitter', 'facebook', 'phone']


class LoginForm(forms.Form):
   username = forms.CharField(max_length = 100,)
   password = forms.CharField(widget=forms.PasswordInput())



# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     class Meta():
#         model = User
#         fields = ('username','password','email')
# class UserProfileInfoForm(forms.ModelForm):
#      class Meta():
#          model = UserProfileInfo
#          fields = ('portfolio_site','profile_pic')


#https://medium.com/@himanshuxd/how-to-create-registration-login-webapp-with-django-2-0-fd33dc7a6c67

#july 2017