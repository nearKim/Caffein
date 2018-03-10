from django.shortcuts import render
from accounts.views import account_index


def index(request):
    print(request)
    if request.user.is_authenticated:
        return account_index(request, request.user)
    else:
        return render(request, 'assets/index.html')
