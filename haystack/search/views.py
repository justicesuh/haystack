from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def searches(request: HttpRequest) -> HttpResponse:
    """Display list of Searches."""
    return render(request, 'search/searches.html')
