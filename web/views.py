import csv
from datetime import datetime

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Min, Max, Avg, Q
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from web.forms import RegistrationForm, AuthForm, FilmForm, ReviewFilterForm, ImportForm
from web.models import MovieRank
from web.services import filter_review, export_reviews_csv, import_reviews_from_csv

User = get_user_model()


@login_required()
def main_view(request):
    reviews = MovieRank.objects.all().order_by('name')
    filter_form = ReviewFilterForm(request.GET)
    filter_form.is_valid()
    filter_review(reviews, filter_form.cleaned_data)
    page = request.GET.get("page", 1)
    paginator = Paginator(reviews, per_page=10)
    if request.GET.get('export') == 'csv':
        response = HttpResponse(
            content_type='text/csv',
            headers={"Content-Disposition": "attachment; filename=reviews.csv"})
        return export_reviews_csv(reviews, response)
    return render(request, 'web/main.html', {'reviews': paginator.get_page(page),
                                             'filter_form': filter_form})


@login_required()
def import_view(request):
    if request.method == 'POST':
        form = ImportForm(files=request.FILES)
        if form.is_valid():
            import_reviews_from_csv(form.cleaned_data['file'], request.user.id)
            return redirect('main')
    return render(request, 'web/import.html', {
        "form": ImportForm()
    })


@login_required()
def analytics_view(request):
    overall_stat = MovieRank.objects.aggregate(
        Count('id'),
        Min('date'),
        Max('date'),
        Avg('score'),
        count_rec=Count('id', filter=Q(is_recommended=True)),
        count_not_rec=Count('id', filter=Q(is_recommended=False))
    )
    date_stat = (
        MovieRank.objects.all()
        .annotate(dates=TruncDate('date'))
        .values('dates')
        .annotate(
            count=Count("id"),
            is_recommended=Count('id', filter=Q(is_recommended=True)),
            avg_score=Avg('score')
        )
        .order_by('-dates')
    )
    return render(request, 'web/analytics.html', {
        "overall_stat": overall_stat,
        'date_stat': date_stat
    })


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, 'web/registration.html', {"form": form, 'is_success': is_success})


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, 'Wrong credentials')
            else:
                login(request, user)
                return redirect("main")
    return render(request, 'web/auth.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect("main")


@login_required
def review_edit_view(request, id=None):
    movierank = get_object_or_404(MovieRank, id=id) if id is not None else None
    form = FilmForm(instance=movierank)
    if request.method == 'POST':
        form = FilmForm(data=request.POST, instance=movierank, initial={'user': request.user})
        if form.is_valid():
            form.save()
            return redirect('main')
    return render(request, 'web/review_form.html', {'form': form})


@login_required
def review_delete_view(request, id=None):
    movierank = get_object_or_404(MovieRank, id=id)
    movierank.delete()
    return redirect('main')
