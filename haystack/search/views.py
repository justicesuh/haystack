from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required
def searches(request: HttpRequest) -> HttpResponse:
    """Display list of Searches."""
    return render(request, 'search/searches.html')
