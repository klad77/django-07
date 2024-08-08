from django.http import HttpResponse

def empty_view(requests):
    return HttpResponse("")


def first_view(request):
    return HttpResponse("<h1>Hello! It's my first view!</h1>")


def second_view(request):
    return HttpResponse("<h1>Hello! It's my second view!</h1>")


def hello_view(request):
    your_name = "Volodymyr"
    return HttpResponse(f"Hello, {your_name} !!")