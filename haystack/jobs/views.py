from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required
def metrics(request: HttpRequest) -> HttpResponse:
    """Display metrics."""
    return render(request, 'jobs/metrics.html')


@login_required
def jobs(request: HttpRequest) -> HttpResponse:
    """Display list of Jobs."""
    return render(request, 'jobs/jobs.html')


@login_required
def companies(request: HttpRequest) -> HttpResponse:
    """Display list of Companies."""
    return render(request, 'jobs/companies.html')
