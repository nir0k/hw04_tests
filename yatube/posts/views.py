from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .constants import POSTS_PER_PAGE
from .forms import PostForm
from .models import Group, Post, User
from .utils import pagi


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_list.html'
    post_list = Post.objects.filter(group=group).order_by('-pub_date')
    context = {
        'title': group.title,
        'page_obj': pagi(request, post_list, POSTS_PER_PAGE),
        'description': group.description,
    }
    return render(
        request,
        template,
        context,
    )


def index(request):
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    post_list = Post.objects.all().order_by('-pub_date')
    context = {
        'title': title,
        'page_obj': pagi(request, post_list, POSTS_PER_PAGE),
    }
    return render(
        request,
        template,
        context
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.author_posts.all().order_by('-pub_date')
    title = 'Профайл пользователя'
    context = {
        'title': title,
        'page_obj': pagi(request, post_list, POSTS_PER_PAGE),
        'author': author,
        'posts_count': post_list.count(),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    posts_count = Post.objects.filter(author=post.author).count()
    context = {
        'post': post,
        'posts_count': posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    if request.method != 'POST':
        form = PostForm()
        return render(
            request,
            template,
            {'form': form},
        )
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.text = form.cleaned_data['text']
        post.save()
        return redirect('posts:profile', request.user)
    return render(
        request,
        template,
        {'form': form},
    )


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    is_edit = True
    post = get_object_or_404(Post, id=post_id)
    groups = Group.objects.all()
    form = PostForm(instance=post)
    context = {
        'form': form,
        'is_edit': is_edit,
        'post_id': post_id,
        'groups': groups,
    }
    if request.method != 'POST':
        return render(
            request,
            template,
            context,
        )
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.text = form.cleaned_data['text']
        post.group = form.cleaned_data['group']
        post.save()
        return redirect('posts:post_detail', post_id)
    return render(
        request,
        template,
        context,
    )
