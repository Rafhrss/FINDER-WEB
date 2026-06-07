from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.reports.serializers import ReportSerializer, ReportWriteSerializer
from apps.reports.selectors import get_report_by_id, list_reports
from apps.reports.services import create_report, delete_report, update_report


class ReportListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        queryset = list_reports(
            status=request.query_params.get("status"),
            location=request.query_params.get("location"),
            keyword=request.query_params.get("q"),
        )
        serializer = ReportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReportWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            report = create_report(user=request.user, **serializer.validated_data)
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        return Response(ReportSerializer(report).data, status=status.HTTP_201_CREATED)


class ReportDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def _get_report(self, report_id):
        report = get_report_by_id(report_id)
        if not report:
            raise NotFound("Laporan tidak ditemukan.")
        return report

    def get(self, request, report_id):
        report = self._get_report(report_id)
        return Response(ReportSerializer(report).data, status=status.HTTP_200_OK)

    def put(self, request, report_id):
        report = self._get_report(report_id)
        serializer = ReportWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            updated_report = update_report(
                report=report,
                actor=request.user,
                **serializer.validated_data,
            )
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        except DjangoPermissionDenied as exc:
            raise PermissionDenied(str(exc)) from exc
        return Response(ReportSerializer(updated_report).data, status=status.HTTP_200_OK)

    def patch(self, request, report_id):
        report = self._get_report(report_id)
        serializer = ReportWriteSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            updated_report = update_report(
                report=report,
                actor=request.user,
                **serializer.validated_data,
            )
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc
        except DjangoPermissionDenied as exc:
            raise PermissionDenied(str(exc)) from exc
        return Response(ReportSerializer(updated_report).data, status=status.HTTP_200_OK)

    def delete(self, request, report_id):
        report = self._get_report(report_id)
        try:
            delete_report(report=report, actor=request.user)
        except DjangoPermissionDenied as exc:
            raise PermissionDenied(str(exc)) from exc
        return Response(status=status.HTTP_204_NO_CONTENT)
