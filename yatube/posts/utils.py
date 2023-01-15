from django.core.paginator import Paginator


def pagi(request, post_list, posts_per_page: int):
    paginator = Paginator(post_list, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
