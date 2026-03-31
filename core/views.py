from django.shortcuts import render
from django.contrib import admin

def home_view(request):
    context = admin.site.each_context(request)

    return render(request, "home.html", context)
