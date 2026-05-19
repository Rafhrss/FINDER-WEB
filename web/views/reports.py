from django.shortcuts import get_object_or_404, render

from apps.reports.models import Report


def report_detail_view(request, report_id: int):
    report = get_object_or_404(Report.objects.select_related("user"), id=report_id)
    return render(request, "web/report_detail.html", {"report": report})
