from django import forms 
from .models import Grupo

class FormGroup (forms.ModelForm):

    class Meta: 
        model = Grupo
        fields = "__all__"