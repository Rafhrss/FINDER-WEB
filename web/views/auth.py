from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from apps.users.forms import LoginForm
from apps.users.services import authenticate_user


def login_view(request):
    if request.user.is_authenticated:
        return redirect("web:home")

    form = LoginForm(request.POST or None)
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST" and form.is_valid():
        try:
            user = authenticate_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
        except ValidationError as exc:
            messages.error(request, " ".join(exc.messages))
        else:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("web:home")

    return render(request, "web/login.html", {"form": form, "next": next_url})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Berhasil logout.")
    return redirect("web:login")
