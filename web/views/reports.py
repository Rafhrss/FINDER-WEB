from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.reports.models import Report, ReportStatus
from apps.reports.services import create_report, update_report


def report_detail_view(request, report_id: int):
    report = get_object_or_404(Report.objects.select_related("user"), id=report_id)

    if request.method == "POST":
        if not request.user.is_authenticated:
            login_url = f"{reverse('web:login')}?{urlencode({'next': request.path})}"
            return redirect(login_url)

        status = request.POST.get("status")
        if not status:
            messages.error(request, "Status laporan tidak boleh kosong.")
            return redirect("web:report-detail", report_id=report_id)

        valid_statuses = {value for value, _ in ReportStatus.choices}
        if status not in valid_statuses:
            messages.error(request, "Status laporan tidak valid.")
            return redirect("web:report-detail", report_id=report_id)

        try:
            update_report(report=report, actor=request.user, status=status)
        except ValidationError as exc:
            messages.error(request, " ".join(exc.messages))
        except PermissionDenied as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, "Status laporan berhasil diperbarui.")

        return redirect("web:report-detail", report_id=report_id)

    return render(
        request,
        "web/report_detail.html",
        {
            "report": report,
            "status_choices": ReportStatus.choices,
        },
    )


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
