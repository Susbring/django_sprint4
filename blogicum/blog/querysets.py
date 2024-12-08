from django.utils import timezone
from django.db.models import Count


def apply_publication_filters(queryset):
    return queryset.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
    )


def apply_publication_annotat(queryset):
    return queryset.annotate(
        comment_count=Count('comments'))
