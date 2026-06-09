from django.conf import settings

def superadmin_emails(request):
    return {"SUPERADMIN_EMAILS": getattr(settings, "SUPERADMIN_EMAILS", [])}
