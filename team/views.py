from django.shortcuts import render

# Create your views here.
from team.ctrl.register import validate


def test(request):
    return render(request, 'team/test.html', {})


def valid_code(request):
    return validate(request)
