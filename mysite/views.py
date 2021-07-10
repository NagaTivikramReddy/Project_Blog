from django.views.generic import CreateView
from django.urls import reverse_lazy
from . import forms


class SignupView(CreateView):
    form_class = forms.SignupForm
    success_url = reverse_lazy("login")
    template_name = "blogs/signup.html"