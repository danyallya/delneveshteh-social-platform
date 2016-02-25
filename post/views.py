from django.shortcuts import render


# Create your views here.
from django.shortcuts import render_to_response


def base(request):
    return render(request, 'base.html', {})


def home(request):
    return render_to_response('home.html')


def post(request):
    return render_to_response('post.html')