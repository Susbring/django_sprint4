from django.core.paginator import Paginator


def paginator(posts, request):
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
