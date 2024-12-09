from django.core.paginator import Paginator


def paginated_page_object(posts, request, posts_per_page=10):
    """Функция возвращает объекты страницы с пагинатаором."""
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
