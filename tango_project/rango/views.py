from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Page




def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context={'categories':category_list}
    return render(request, 'rango/index.html', context)


def show_category(request, category_url):
    context = {}
    try:
        category = Category.objects.get(slug=category_url)
        pages = Page.objects.filter(category=category)
        context['pages']=pages
        context['category']=category
    except Category.DoesNotExist:
        context['category'] = None
        context['pages'] = None
    return render(request, "rango/category.html", context)

