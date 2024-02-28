from django.shortcuts import render, redirect


def index_page(request):
    return render(request, 'index.html')


def logginpage(request):
    context = {}
    if request.method == 'POST':

        return redirect(request, 'index.html')
    return render(request, 'loggin.html', context)