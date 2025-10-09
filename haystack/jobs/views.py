from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def jobs(request: HttpRequest) -> HttpResponse:
    """Display list of Jobs."""
    return render(request, 'jobs/jobs.html')


def companies(request: HttpRequest) -> HttpResponse:
    """Display list of Companies."""
    return render(request, 'jobs/companies.html')
