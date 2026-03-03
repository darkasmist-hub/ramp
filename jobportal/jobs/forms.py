from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ["employer", "created_at"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })