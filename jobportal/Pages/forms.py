from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    
  skills = forms.CharField(
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Python, Django, JavaScript, SQL'
    }),
    help_text="Enter skills separated by commas"
)
  hobbys = forms.CharField(
    widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 4,
        'placeholder': 'Your hobbies'
    }),
    required=False
)
  languages = forms.CharField(
    widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 1,
        'placeholder': 'Your languages'
    }),
    required=False
)
  class Meta:
    model = Resume
    fields = [
            'full_name', 'email', 'phone', 'location',
            'skills', 'languages', 'hobbys',
            'summary', 'experience', 'education',
            'image', 'template'
        ]
    widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your skills'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your summary'
            }),
            'experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your experience'
            }),
            'education': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your education'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your location'
            }),
            
        }