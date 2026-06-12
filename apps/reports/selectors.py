from django.db.models import Q, Count
from apps.reports.models import Report, ReportStatus


def get_user_report_statistics(user) -> dict:
    stats = Report.objects.filter(user=user).values("status").annotate(count=Count("id"))
    result = {
        ReportStatus.LOST.lower(): 0,
        ReportStatus.FOUND.lower(): 0,
        ReportStatus.CLAIMED.lower(): 0,
    }
    for stat in stats:
        status_key = stat["status"].lower()
        if status_key in result:
            result[status_key] = stat["count"]
    return result


def list_reports(
    *,
    status: str | None = None,
    location: str | None = None,
    keyword: str | None = None,
):
    queryset = Report.objects.select_related("user").all()
    if status:
        queryset = queryset.filter(status=status)
    if location:
        queryset = queryset.filter(location__icontains=location)
    if keyword:
        queryset = queryset.filter(
            Q(title__icontains=keyword) |
            Q(location__icontains=keyword) |
            Q(description__icontains=keyword)
        )
    return queryset.order_by("-created_at")


def get_report_by_id(report_id) -> Report | None:
    return Report.objects.select_related("user").filter(id=report_id).first()


def get_reports_by_owner(user):
    return Report.objects.filter(user=user).annotate(
        chat_rooms_count=Count("chat_rooms")
    ).order_by("-created_at")
