from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.reports.models import ReportStatus
from apps.reports.selectors import get_reports_by_owner


@login_required
def profile_view(request):
    reports = get_reports_by_owner(request.user)
    lost_count = reports.filter(status=ReportStatus.LOST).count()
    found_count = reports.filter(status=ReportStatus.FOUND).count()
    claimed_count = reports.filter(status=ReportStatus.CLAIMED).count()
    
    return render(
        request,
        "web/profile.html",
        {
            "profile_user": request.user,
            "reports": reports,
            "lost_count": lost_count,
            "found_count": found_count,
            "claimed_count": claimed_count,
        },
    )
