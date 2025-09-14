from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя пользователя',
            'class': 'form-control',
            'id': 'id_username'  # id для согласованности, но LoginView тоже создаёт id
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', 'class': 'form-control', 'id': 'id_password1'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль', 'class': 'form-control', 'id': 'id_password2'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'photo']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 2 * 1024 * 1024:  # 2 MB
                raise forms.ValidationError("Размер фото не должен превышать 2 МБ.")
            ext = photo.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'bmp']:
                raise forms.ValidationError("Недопустимый формат файла. Разрешены: jpg, jpeg, png, bmp.")
        return photo
