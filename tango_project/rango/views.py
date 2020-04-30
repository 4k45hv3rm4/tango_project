from datetime import datetime
from django.urls import reverse
from django.shortcuts import render
from .models import Category, Page
from django.contrib.auth.decorators import login_required
from tango_project.settings import LOGIN_REDIRECT_URL
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout , login
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm


# helper functions

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val=default_val
    return val


def visitor_cookie_handler(request):

    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time ).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


#home page
def index(request):
    category_list = Category.objects.order_by('-likes')[:10]
    page_list = Page.objects.order_by('-views')[:5]
    context={'categories':category_list}

    visitor_cookie_handler(request)
    context['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context)
    return response

# register
def register(request):
    registered=False

    if request.method=='POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)


        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
            print("registered")

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
                'rango/register.html',
                {
                'user_form':user_form,
                'profile_form':profile_form,
                'registered':registered
                }
            )



def user_login(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Your rango account is disabled')
        else:
            print("Invalid login details {username}, {password}")
            return render(request, 'rango/Invalid.html', {'message':'Invalid Login Details Supplied'})
    else:
        return render(request, 'rango/login.html', {})

@login_required(login_url=LOGIN_REDIRECT_URL)
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))




# Displays category
@login_required(login_url=LOGIN_REDIRECT_URL)
def show_category(request, category_url):
    context = {}
    try:
        category = Category.objects.get(slug=category_url)
        pages = Page.objects.filter(category=category)
        context['pages']=pages
        context['category_url'] = category_url
        context['category']=category
    except Category.DoesNotExist:
        context['category'] = None
        context['pages'] = None
    return render(request, "rango/category.html", context)

# add category
@login_required(login_url=LOGIN_REDIRECT_URL)
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return index(request)

        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

# add page
@login_required(login_url=LOGIN_REDIRECT_URL)
def add_page(request, category_url):
    try:
        category = Category.objects.get(slug=category_url)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method=='POST':
        form=PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views
                page.save()
                return show_category(request, category_url)
            else:
                print(form.errors)
    context = {'form':form, 'cat': category}
    return render(request, 'rango/add_page.html', context)


