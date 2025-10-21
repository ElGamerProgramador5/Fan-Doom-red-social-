from django import forms
from .models import Profile, Work

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'cover_image', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Cuéntanos un poco sobre ti...'}),
            'profile_image': forms.FileInput(),
            'cover_image': forms.FileInput(),
        }

class WorkForm(forms.ModelForm):
    GENRE_CHOICES = [
        ('', '---------'),
        ('Fanfic', 'Fanfic'),
        ('Análisis', 'Análisis'),
        ('Teoría', 'Teoría'),
        ('Arte', 'Arte'),
        ('Otro', 'Otro'),
    ]
    AUDIENCE_CHOICES = [
        ('', '---------'),
        ('Todo Público', 'Todo Público'),
        ('Jóvenes', 'Jóvenes'),
        ('Adultos', 'Adultos'),
    ]

    genre = forms.ChoiceField(choices=GENRE_CHOICES, required=True, label="Género")
    target_audience = forms.ChoiceField(choices=AUDIENCE_CHOICES, required=True, label="Público Dirigido")

    class Meta:
        model = Work
        fields = ['title', 'description', 'genre', 'target_audience']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'El título de tu magnífica obra'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe tu obra, de qué trata, cuál es su universo...'}),
        }
        labels = {
            'title': 'Título',
            'description': 'Descripción',
        }