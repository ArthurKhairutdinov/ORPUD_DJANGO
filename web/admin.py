from django.contrib import admin

# Register your models here.
from web.models import MovieRank


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'date', 'score', 'review', 'is_recommended')
    search_fields = ('id', 'name', 'review')
    list_filter = ('date', 'is_recommended', 'score')


admin.site.register(MovieRank, ReviewAdmin)
