from django.contrib import admin
from django.urls import path

from web.views import main_view, registration_view, auth_view, logout_view, review_edit_view, review_delete_view, \
    analytics_view, import_view

urlpatterns = [
    path('', main_view, name='main'),
    path('import/', import_view, name='import'),
    path('reg/', registration_view, name='reg'),
    path('auth/', auth_view, name='auth'),
    path('logout/', logout_view, name='logout'),
    path('review/add', review_edit_view, name='review_add'),
    path('review/<int:id>', review_edit_view, name='review_edit'),
    path('review/<int:id>/delete/', review_delete_view, name='review_delete'),
    path('analytics/', analytics_view, name='analytics')

]
