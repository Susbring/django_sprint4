from django.core.paginator import Paginator

from .constants import NUMBER_OF_RECORDS_ON_THE_PAGE


def paginated_page_object(
        posts,
        request,
        posts_per_page=NUMBER_OF_RECORDS_ON_THE_PAGE):
    """Функция возвращает объекты страницы с пагинатаором."""
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
