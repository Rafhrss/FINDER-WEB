from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

from apps.reports.models import ReportStatus
from apps.reports.selectors import list_reports
from apps.reports.ai_services import extract_keywords_with_gemini, analyze_matches_with_gemini


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


def ai_search_view(request):
    """
    Endpoint for AJAX semantic AI search using Gemini.
    """
    query = request.GET.get("q", "")
    status_filter = request.GET.get("filter", "")
    
    if not query:
        return JsonResponse({"error": "Query is required"}, status=400)
        
    try:
        # 1. Extract keywords as a list
        extracted = extract_keywords_with_gemini(query)
        keywords_list = extracted.get("keywords", [query])
        
        # 2. Search database with extracted keywords (OR logic)
        from django.db.models import Q
        
        reports_qs = list_reports(
            status=status_filter if status_filter else None,
        )
        
        if keywords_list:
            q_objects = Q()
            for kw in keywords_list:
                q_objects |= Q(title__icontains=kw) | Q(location__icontains=kw) | Q(description__icontains=kw)
            reports_qs = reports_qs.filter(q_objects).distinct()
        
        # Take top 15 matches to limit context window for AI
        reports_list = list(reports_qs[:15])
        
        if not reports_list:
            html = render_to_string("partials/_ai_report_card_list.html", {"reports": [], "query": query})
            return JsonResponse({"html": html, "count": 0})
            
        # 3. Analyze matches with AI
        analyzed_reports = analyze_matches_with_gemini(query, reports_list)
        
        # 4. Render HTML template with results
        html = render_to_string(
            "partials/_ai_report_card_list.html", 
            {"reports": analyzed_reports, "query": query}
        )
        
        return JsonResponse({
            "html": html,
            "count": len(analyzed_reports)
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
