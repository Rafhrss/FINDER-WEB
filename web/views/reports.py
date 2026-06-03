from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.reports.models import Report, ReportStatus
from apps.reports.services import create_report


def report_detail_view(request, report_id: int):
    report = get_object_or_404(Report.objects.select_related("user"), id=report_id)
    return render(request, "web/report_detail.html", {"report": report})


@login_required
def report_create_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        status = request.POST.get("status")
        location = request.POST.get("location")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        if not all([title, status, location, description]):
            messages.error(request, "Mohon lengkapi semua bidang yang wajib diisi.")
            return render(request, "web/report_create.html", {"request_post": request.POST})

        try:
            report = create_report(
                user=request.user,
                title=title,
                description=description,
                location=location,
                image=image,
                status=status,
            )
            messages.success(request, "Laporan berhasil diterbitkan!")
            return redirect("web:report-detail", report_id=report.id)
        except Exception as e:
            messages.error(request, f"Gagal membuat laporan: {str(e)}")
            return render(request, "web/report_create.html", {"request_post": request.POST})

    return render(request, "web/report_create.html")
