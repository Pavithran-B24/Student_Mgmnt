from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Document, Students
from django.contrib.auth.models import User

# class RegisterForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'password']

#         widgets = {
#             'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
#             'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
#             'username': forms.TextInput(attrs={'placeholder': 'User Name'}),
#             'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
#         }

# class LoginForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']

#         widgets = {
#             'username': forms.TextInput(attrs={'placeholder': 'User Name'}),
#             'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
#         }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = '__all__'
        labels = {
            'fullname': 'Full Name',
            'role_no': 'Roll Number',
            'email': 'Email ID',
            'mobile': 'Mobile Number',
            'degree': 'Degree',
            'dept': 'Department',
        }
        widgets = {
            'fullname': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'role_no': forms.NumberInput(attrs={'placeholder': 'Roll Number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email ID'}),
            'mobile': forms.NumberInput(attrs={'placeholder': 'Mobile Number'}),
            'degree': forms.TextInput(attrs={'placeholder': 'Degree'}),
            'dept': forms.TextInput(attrs={'placeholder': 'Department'}),
        }

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('myfile',)
       