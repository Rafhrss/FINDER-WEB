from django.core.paginator import Paginator
from django.shortcuts import render

from apps.reports.models import ReportStatus
from apps.reports.selectors import list_reports


def search_view(request):
    keyword = request.GET.get("q", "")
    status_filter = request.GET.get("filter", "")

    reports = list_reports(
        status=status_filter if status_filter else None,
        keyword=keyword if keyword else None,
    )

    paginator = Paginator(reports, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "selected_keyword": keyword,
        "selected_filter": status_filter,
    }
    return render(request, "web/search.html", context)
