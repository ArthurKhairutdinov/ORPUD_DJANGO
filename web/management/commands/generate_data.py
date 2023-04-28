from datetime import timedelta
from random import  randint, choice

from django.core.management import BaseCommand
from django.utils.timezone import now

from web.models import MovieRank, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.first()
        time_now = now()
        ranks = []
        for i in range(25):
            ranks.append(MovieRank(
                name=f'generated{i}',
                is_recommended = choice((True,False)),
                review = f'review{i}',
                score = randint(0,10),
                user = user,
                date = time_now - timedelta(hours=i)
            ))

        MovieRank.objects.bulk_create(ranks)