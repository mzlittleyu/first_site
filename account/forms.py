# CODING=UTF-8
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile,UserInfo
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
class User_RegistrationForm(forms.ModelForm):
    password = forms.CharField(label= "Password" ,widget=forms.PasswordInput)
    password_again= forms.CharField(label="Confirm password",widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username","email")
    def clean_password_again(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_again']:
            raise forms.ValidationError("oh,different passwords")
        return cd['password_again']
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone","birth")
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school","company","profession","address","aboutme","photo",)
class UserForm(forms.ModelForm):#单独建立一个表格使不能更改用户名
    class Meta:
        model = User
        fields = ("email",)
