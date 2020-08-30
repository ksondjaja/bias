from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms
from django.contrib import messages
from . import util
import urllib

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
            if len(output)==3:
                return render(request, "api/bias.html",{
                    "author": output[0],
                    "title": output[1],
                    "text": output[2],
                    "news": news,
                    "score": score
                })
            else:
                return render(request,"api/bias.html",{
                    "message": "News article is invalid or cannot be read"
                })
