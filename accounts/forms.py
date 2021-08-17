from PIL import Image
from boards.models import Blogger, Categories, Reader

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class DateInput(forms.DateInput):
    input_type = 'date'


class BloggerRegisterForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Categories.objects.all(), required=False)

    class Meta:
        model = Blogger
        fields = ['birthday', 'country', 'city', 'categories']
        widgets = {
            'birthday': DateInput(),

        }


class BloggerUpdate(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Categories.objects.all(), required=False)
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Blogger
        fields = ['avatar', 'x', 'y', 'width', 'height', 'birthday', 'country', 'city', 'categories']
        widgets = {
            'birthday': DateInput(),
            'avatar': forms.FileInput(attrs={
                'accept': 'image/*',
                'style': 'padding-left: 44%;'
            })
        }

    def save(self, commit=True):
        photo = super(BloggerUpdate, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        if x and y and w and h:
            image = Image.open(photo.avatar)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            resized_image.save(photo.avatar.path)
        return photo







class ReaderRegisterForm(forms.ModelForm):

    class Meta:
        model = Reader
        fields = ['adult', 'interests']


class ReaderUpdate(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Reader
        fields = ['avatar', 'x', 'y', 'width', 'height', 'adult', 'interests']
        # exclude = ['x', 'y', 'width', 'height']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'accept': 'image/*',
                'style': 'padding-left: 44%;'

            })
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        photo = super(ReaderUpdate, self).save(commit=True)
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        if x and y and w and h:
            image = Image.open(photo.avatar)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            resized_image.save(photo.avatar.path)

        return photo


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", 'last_name', 'email')