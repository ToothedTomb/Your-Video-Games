from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name','game_company', 'about', 'realise_date', 'platform', 'genre', 'rating', 'comment', 'screenshot']  # Removed 'user'
        widgets = {
            'game_company': forms.TextInput(attrs={'class': 'form-control'}),  
            'about': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'realise_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'platform': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
            'game_company': forms.TextInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'name': 'Game Name',
            'about': 'About the Game',
            'realise_date': 'Release Date',
            'platform': 'Platform',
            'genre': 'Genre',
            'rating': 'Rating (1-10)',
            'comment': 'Your Comment',
            'screenshot': 'Screenshot',
            'game_company': 'Game Company',
        }