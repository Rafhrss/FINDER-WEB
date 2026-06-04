from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Berhasil logout.")
    return redirect("web:home")
