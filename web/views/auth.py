from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect, render


def login_view(request):
    if request.user.is_authenticated:
        return redirect("web:home")

    next_url = request.GET.get("next", "")
    query_params = {"process": "login"}
    if next_url:
        query_params["next"] = next_url
    google_login_url = f"{reverse('google_login')}?{urlencode(query_params)}"
    return render(
        request,
        "web/login.html",
        {"next": next_url, "google_login_url": google_login_url},
    )


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Berhasil logout.")
    return redirect("web:login")
