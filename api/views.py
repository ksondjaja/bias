from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util

# Create your views here.

class NewURLForm(forms.Form):
    news = forms.CharField(label="News URL")

def index(request):
    return render(request, "api/index.html")

def lookup(request):
    if request.method == "POST":
        article = NewURLForm(request.POST)
        if article.is_valid():
            news = article.cleaned_data["news"]
            output = util.getStuff(news)
            score = util.getBiasIndex(news)
            return render (request, "api/bias.html",{
                "author": output[0],
                "title": output[1],
                "news": news,
                "score": score
            })