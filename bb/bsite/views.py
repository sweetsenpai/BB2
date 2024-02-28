from django.shortcuts import render, redirect


def index_page(request):
    return render(request, 'index.html')


def logginpage(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get('username') == 'pro' and request.POST.get('password') == 'pro':
            return redirect('index_page')
    return render(request, 'loggin.html', context)