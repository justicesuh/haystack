from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Display metrics."""
    metrics = [
        {
            'title': 'Today',
            'count': 20,
            'goal': 32,
            'delta': -2,
            'progress': 63,
        },
        {
            'title': 'Last 7 Days',
            'count': 125,
            'goal': 224,
            'delta': 7,
            'progress': 56,
        },
        {
            'title': 'Last 30 Days',
            'count': 633,
            'goal': 960,
            'delta': 15,
            'progress': 66,
        },
        {
            'title': 'Total',
            'count': 2914,
            'goal': 0,
            'delta': 0,
            'progress': 0,
        },
    ]

    return render(request, 'metrics/dashboard.html', {'metrics': metrics})
