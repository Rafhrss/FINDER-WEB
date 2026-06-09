from django.core.exceptions import ValidationError

from apps.core.exceptions import OwnershipValidationError
from apps.reports.models import Report, ReportStatus
from apps.core.supabase_client import upload_image_to_supabase


def validate_image(image_file):
    if not image_file:
        return
    if image_file.size > 5 * 1024 * 1024:
        raise ValidationError("Ukuran file gambar tidak boleh melebihi 5MB.")
    allowed_types = ["image/jpeg", "image/jpg", "image/png"]
    if image_file.content_type not in allowed_types:
        raise ValidationError("Format gambar harus berupa JPG, JPEG, atau PNG.")


from django.conf import settings

def ensure_report_owner(*, report: Report, actor) -> None:
    superadmins = getattr(settings, "SUPERADMIN_EMAILS", [])
    if report.user_id != actor.id and actor.email not in superadmins:
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
    image_url = None
    if image:
        validate_image(image)
        try:
            image_url = upload_image_to_supabase(image)
        except Exception as e:
            raise ValidationError(f"Gagal mengunggah gambar: {str(e)}")

    report = Report(
        user=user,
        title=title.strip(),
        description=description.strip(),
        location=location.strip(),
        image=image_url,
        status=status,
    )
    report.full_clean()
    report.save()
    return report


def update_report(*, report: Report, actor, **kwargs) -> Report:
    ensure_report_owner(report=report, actor=actor)

    if "image" in kwargs and kwargs["image"] is not None:
        image_file = kwargs["image"]
        if not isinstance(image_file, str):
            validate_image(image_file)
            try:
                kwargs["image"] = upload_image_to_supabase(image_file)
            except Exception as e:
                raise ValidationError(f"Gagal mengunggah gambar: {str(e)}")

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
