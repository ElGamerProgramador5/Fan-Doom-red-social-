from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'cover_image', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Cuéntanos un poco sobre ti...'}),
            'profile_image': forms.FileInput(),
            'cover_image': forms.FileInput(),
        }