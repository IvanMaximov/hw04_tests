from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from yatube.settings import PAGE_COUNT

from .models import Group, Post, User
from .forms import PostForm


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    post = get_object_or_404(User, username=username)
    posts = post.posts.all()
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'post': post,
        'page_obj': page_obj,
        'number_of_posts': posts.count(),
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post_detail = get_object_or_404(Post, pk=post_id)
    author = post_detail.author
    number_of_posts = author.posts.all().count()
    context = {
        'post_detail': post_detail,
        'number_of_posts': number_of_posts,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    if request.method != 'POST':
        form = PostForm()
        return render(request, 'posts/create.html', {'form': form})
    form = PostForm(request.POST)
    if not form.is_valid():
        return render(request, 'posts/create.html', {'form': form})
    form.instance.author = request.user
    form.save()
    return redirect('posts:profile', request.user.username)


@login_required
def post_edit(request, post_id):
    post_edit = get_object_or_404(Post, pk=post_id)
    if request.method != 'POST':
        form = PostForm(instance=post_edit)
        return render(
            request, 'posts/create.html',
            {'form': form, 'is_edit': post_edit}
        )
    form = PostForm(request.POST, instance=post_edit)
    if not form.is_valid():
        return render(request, 'posts/create.html', {'form': form})
    form.save()
    return redirect('posts:post_detail', post_id)
