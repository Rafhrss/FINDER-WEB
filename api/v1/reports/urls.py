from django.urls import path

from api.v1.reports.views import ReportDetailAPIView, ReportListCreateAPIView

urlpatterns = [
    path("", ReportListCreateAPIView.as_view(), name="report-list-create"),
    path("<uuid:report_id>/", ReportDetailAPIView.as_view(), name="report-detail"),
]
