from django.shortcuts import render

from apps.reports.models import ReportStatus
from apps.reports.selectors import list_reports


def home_view(request):
    reports = list_reports(
        status=request.GET.get("status"),
        location=request.GET.get("location"),
        keyword=request.GET.get("q"),
    )
    context = {
        "reports": reports,
        "statuses": ReportStatus.choices,
        "selected_status": request.GET.get("status", ""),
        "selected_location": request.GET.get("location", ""),
        "selected_keyword": request.GET.get("q", ""),
    }
    return render(request, "web/home.html", context)
