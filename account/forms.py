from django import forms
from django.contrib.auth.models import User
from .models import Services, ServiceRatings


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']


class InterCityForm(forms.Form):
    origin = forms.CharField(max_length=100,
                                widget=forms.TextInput(
                                    attrs={
                                        'style': 'width: 400px;',
                                        'placeholder': 'Your Current Location'
                                    }
                                ))
    destination = forms.CharField(max_length=100,
                                  widget=forms.TextInput(
                                      attrs={
                                          'style': 'width: 400px;',
                                          'placeholder': 'Where You Want to Go?'
                                      }
                                  )
                                  )


class CityBusForm(forms.Form):
    origin = forms.CharField(max_length=100,
                             widget=forms.TextInput(
                                    attrs={
                                        'style': 'width: 400px;',
                                        'placeholder': 'Your Current Location'
                                    }
                                ))
    destination = forms.CharField(max_length=100,
                                  widget=forms.TextInput(
                                      attrs={
                                          'style': 'width: 400px;',
                                          'placeholder': 'Where You Want to Go?'
                                      }
                                  )
                                  )


class ServiceAddForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ('name', 'service_type', 'contact', 'latitude',
                    'longitude', 'address')


class DeleteServiceForm(forms.Form):
    service_id = forms.IntegerField()


class SearchForm(forms.Form):
    strr = forms.CharField(max_length=50)


class SearchIndividualForm(forms.Form):
    id = forms.IntegerField()

class RateServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceRatings
        fields = ['rating', ]


