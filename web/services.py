import csv

from web.models import MovieRank


def filter_review(reviews, filters: dict):
    if filters['search']:
        reviews = reviews.filter(name__icontains=filters['search'])

    if filters['is_recommended'] is not None:
        reviews = reviews.filter(is_recommended=filters['is_recommended'])

    if filters['start_date']:
        reviews = reviews.filter(date__gte=filters['start_date'])

    if filters['end_date']:
        reviews = reviews.filter(date__lte=filters['end_date'])

    if filters['score']:
        reviews = reviews.filter(score=filters['score'])
    return reviews


def export_reviews_csv(reviews, responce):
    writer = csv.writer(responce)
    writer.writerow(('name', 'date', 'is_recommended', 'score', 'review'))
    for review in reviews:
        writer.writerow((review.name, review.date, review.is_recommended, review.score, review.review))
    return responce


def import_reviews_from_csv(file, user_id):
    str_from_file = (row.decode() for row in file)
    reader = csv.DictReader(str_from_file)
    reviews = []
    for row in reader:
        reviews.append(MovieRank(
            name=row['name'],
            date=row['date'],
            is_recommended=row['is_recommended'],
            score=row['score'],
            review=row['review'],
            user_id=user_id
        ))
    saved_reviews = MovieRank.objects.bulk_create(reviews)
