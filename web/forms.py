import datetime

from django import forms
from django.contrib.auth import get_user_model

from web.models import MovieRank

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password']:
            self.add_error('password', 'Password mismatch')
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class FilmForm(forms.ModelForm):
    class Meta:
        model = MovieRank
        fields = ('name', 'score', 'review', 'is_recommended')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['score'] not in range(1, 11):
            self.add_error('score', 'Wrong score')
        return cleaned_data

    def save(self, commit=True):
        self.instance.date = datetime.datetime.now()
        self.instance.user = self.initial['user']
        return super().save(commit)


class ReviewFilterForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Поиск'}), required=False, label='Название')
    is_recommended = forms.NullBooleanField(label='Рекомендован', required=False)
    start_date = forms.DateTimeField(label='От',
                                     widget=forms.DateTimeInput(attrs={'type': "datetime-local"},
                                                                format='%Y-%m-%DT%H:%M'), required=False)
    end_date = forms.DateTimeField(label='До',
                                   widget=forms.DateTimeInput(attrs={'type': "datetime-local"},
                                                              format='%Y-%m-%DT%H:%M'), required=False)
    score = forms.IntegerField(max_value=10, min_value=1, required=False)


class ImportForm(forms.Form):
    file = forms.FileField()
