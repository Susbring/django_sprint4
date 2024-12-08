from django.utils import timezone
from django.db.models import Count


def apply_publication_filters(queryset):
    """Реализация фильтров на кварисеты."""
    return queryset.select_related(
        'category',
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


def apply_publication_annotat(queryset):
    """Реализация аннотаций на кварисеты."""
    return queryset.annotate(
        comment_count=Count('comments')).order_by('-pub_date')
