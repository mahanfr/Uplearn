from django.shortcuts import render
from .forms import UserRegisterForm


def register_view(request):
    return render(request, "accounts/register.html", context={'form': UserRegisterForm})