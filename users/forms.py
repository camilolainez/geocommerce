from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.urls import reverse

class CustomUserCreationForm(UserCreationForm):
    #check_username_url = reverse('users:check_username')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.TextInput(attrs={'type':'email', 'name': 'email', 'id': 'email', 'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'name@company.com', 'hx-trigger': 'change', 'hx-post': 'registration/register.html', 'hx-target': '#email-error'}),)
    username = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'type': 'username', 'name': 'username', 'id': 'username', 'class': 'hidden bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}),)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        check_username_url = reverse('users:check_username')
        # Atributos CSS para los campos del formulario
        self.fields['username'].widget.attrs.update({'type': 'username', 'name': 'username', 'id': 'username', 'class': 'hidden bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['email'].widget.attrs.update({'type':'email', 'name': 'email', 'id': 'email', 'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'placeholder': 'name@company.com', 'hx-trigger': 'change', 'hx-post': check_username_url, 'hx-target': '#email-error'})        
        self.fields['password1'].widget.attrs.update({'type': 'password', 'name':'password1', 'id': 'password', 'placeholder': '••••••••', 'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['password2'].widget.attrs.update({'type': 'password', 'name':'password2','class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 'id': 'password_repeat','placeholder': '••••••••'})

    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        password_repeat = cleaned_data.get('password2')

        if password and password_repeat and password != password_repeat:
            self.add_error('password2', "Las contraseñas no coinciden.")

        return cleaned_data
