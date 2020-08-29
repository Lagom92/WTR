from django.shortcuts import redirect, render
from .models import Webtoon
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def main(request):
    
    return render(request, 'board/main.html')


def choice(request):
    webtoon_list = Webtoon.objects.all()

    # Pagination
    paginator = Paginator(webtoon_list, 36) # Show 33 contacts per page
    page = request.GET.get('page')
    try:
        webtoons= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        webtoons = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        webtoons = paginator.page(paginator.num_pages)

    return render(request, 'board/choice.html', {'webtoons': webtoons})


def recommend(request):

    return render(request, 'board/recommend.html')