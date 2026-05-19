from django.contrib import admin

from apps.reports.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "status", "location", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description", "location", "user__email")
