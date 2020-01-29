from django import forms
from .models import Contact
from django.core import validators
from django.forms import ModelForm, TextInput, RegexField, Textarea, CharField


# Форма отправки для записи
class ContactForm( ModelForm ):
    #phone_number = RegexField(
     #   regex=r'^\+?1?\d{9,15}$')
        #error_message=("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
         #              ) )

    class Meta:
        model = Contact
        fields = ['name', 'last_name', 'phone_number', 'message']
        widgets = {
        'name': TextInput( attrs={
            'class': 'form-control input',
            'id': 'fff',
            'type': 'text',
             }),
        'phone_number': TextInput( attrs={
            'class': 'form-control',
            'id': 'phone-input'} ),
        "last_name": TextInput( attrs={
            "class": 'form-control',
            'id': 'fff',
            'type': 'text'}
             ),

        "message": Textarea( attrs={
            'class': 'form-control',
            'type': 'text',
            'name': 'message',
            'id': 'fff'
            })
        }