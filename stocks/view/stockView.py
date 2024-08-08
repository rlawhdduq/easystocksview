import random as rd
import matplotlib.pyplot as plt

from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO


def stock(request):
    temp = []
    for i in range(30):
        tempor = round(rd.uniform(6, 14), 1)
        temp.insert(i, tempor)
    x = list(range(1, len(temp)+1))
    plt.figure(figsize=(13, 6))
    plt.plot(x, temp, 'ro--', label='기본그래프')
    plt.title('3월 기온')
    plt.xlabel('날짜')
    plt.ylabel('온도')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return HttpResponse(buf.read(), content_type='image/png')
