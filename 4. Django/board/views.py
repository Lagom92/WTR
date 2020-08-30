from django.shortcuts import redirect, render
from .models import Webtoon
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from predict import predict_func


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
    wt_id = request.POST['wt_id']
    recommend_list = predict_func(wt_id)

    if recommend_list:
        wt_data1 = Webtoon.objects.get(wt_id=recommend_list[0])
        wt_data2 = Webtoon.objects.get(wt_id=recommend_list[1])
        wt_data3 = Webtoon.objects.get(wt_id=recommend_list[2])

        context = {
            'have_data': True,
            'wt_data1': wt_data1,
            'wt_data2': wt_data2,
            'wt_data3': wt_data3,
        }
    else:
        context = {
            'have_data': False

        }

    return render(request, 'board/recommend.html', context)