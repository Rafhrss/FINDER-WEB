from apps.reports.models import Report


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
        queryset = queryset.filter(title__icontains=keyword)
    return queryset


def get_report_by_id(report_id: int) -> Report | None:
    return Report.objects.select_related("user").filter(id=report_id).first()


def get_reports_by_owner(user):
    return Report.objects.filter(user=user).order_by("-created_at")
