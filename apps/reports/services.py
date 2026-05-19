from django.core.exceptions import ValidationError

from apps.core.exceptions import OwnershipValidationError
from apps.reports.models import Report, ReportStatus


def ensure_report_owner(*, report: Report, actor) -> None:
    if report.user_id != actor.id:
        raise OwnershipValidationError("Hanya pemilik laporan yang bisa mengubah data.")


def create_report(
    *,
    user,
    title: str,
    description: str,
    location: str,
    image=None,
    status: str = ReportStatus.LOST,
) -> Report:
    report = Report(
        user=user,
        title=title.strip(),
        description=description.strip(),
        location=location.strip(),
        image=image,
        status=status,
    )
    report.full_clean()
    report.save()
    return report


def update_report(*, report: Report, actor, **kwargs) -> Report:
    ensure_report_owner(report=report, actor=actor)

    for field in ("title", "description", "location", "image", "status"):
        if field in kwargs and kwargs[field] is not None:
            value = kwargs[field]
            if field in {"title", "description", "location"} and isinstance(value, str):
                value = value.strip()
            setattr(report, field, value)

    report.full_clean()
    report.save()
    return report


def delete_report(*, report: Report, actor) -> None:
    ensure_report_owner(report=report, actor=actor)
    report.delete()


def validate_report_exists(report: Report | None) -> Report:
    if not report:
        raise ValidationError("Laporan tidak ditemukan.")
    return report
