from django.shortcuts import render

from apps.reports.models import ReportStatus
from apps.reports.selectors import list_reports


def home_view(request):
    reports = list_reports()[:6]
    context = {
        "reports": reports,
    }
    return render(request, "web/home.html", context)


def terms_of_service_view(request):
    return render(request, "terms_of_service.html")

def about_view(request):
    return render(request, "web/about.html")
