from django.shortcuts import render

from apps.reports.models import ReportStatus
from apps.reports.selectors import list_reports


def home_view(request):
    reports = list_reports(status=ReportStatus.LOST)[:6]
    context = {
        "reports": reports,
    }
    return render(request, "web/home.html", context)
