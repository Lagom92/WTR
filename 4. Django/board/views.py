from django.shortcuts import redirect, render

def main(request):

    return render(request, 'board/main.html')


def choice(request):

    return render(request, 'board/choice.html')

def recommend(request):

    return render(request, 'board/recommend.html')