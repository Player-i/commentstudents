from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Form to create user
from .forms import UserRegistrationForm, PostForm, CommentForm, EmailLoginForm
from .models import Post, Comment
from django.contrib.auth import authenticate, login

from django.contrib.auth import logout
from django.db.models import Count
# Create your views here.

def home(request):
    context = {}
    posts = Post.objects.all().order_by("-id")
    comments = Comment.objects.all().order_by('-id')
    context["posts"] = posts
    context['comments'] = comments
    if request.user.is_authenticated:
        user = request.user
        context["user"] = user
    return render(request, "home.html", context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Name use in urls.py
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home') 

    if request.method == 'POST':
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or perform any other desired actions
                return redirect('home')  # Replace 'home' with your desired URL name
            else:
                # Authentication failed
                form.add_error(None, 'Invalid email or password.')
    else:
        form = EmailLoginForm()
    
    return render(request, 'login.html', {'form': form})


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'create.html', context)


def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        content = request.POST['content']
        author = request.user  # Assuming the user is authenticated
        comment = Comment.objects.create(post=post, author=author, content=content)
        return redirect('home')

    return redirect('home')

def post_detail(request, post_id):
    context = {}
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.all().order_by('-id')
    context['comments'] = comments
    context['post'] = post
    print(comments)
    return render(request, "post.html", context=context)


def logout_view(request):
    logout(request)
    return redirect('home')

def search_post(request):
    search_query = request.GET.get('search_query', '')

    # Perform the search query
    posts = Post.objects.filter(caption__icontains=search_query)
    comments = Comment.objects.all().order_by('-id')
    
    context = {
        'posts': posts,
        'search_query': search_query,
        'comments': comments,
    }

    return render(request, 'search_results.html', context)

def top(request):
    # Retrieve posts ordered by the number of comments in descending order
    posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')


    context = {}
    comments = Comment.objects.all().order_by('-id')
    context["posts"] = posts
    context['comments'] = comments
    if request.user.is_authenticated:
        user = request.user
        context["user"] = user
    return render(request, 'top.html', context)