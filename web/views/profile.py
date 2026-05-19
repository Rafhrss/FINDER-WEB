from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.reports.selectors import get_reports_by_owner


@login_required
def profile_view(request):
    reports = get_reports_by_owner(request.user)
    return render(
        request,
        "web/profile.html",
        {
            "profile_user": request.user,
            "reports": reports,
        },
    )
