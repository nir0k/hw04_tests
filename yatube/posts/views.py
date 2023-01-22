from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .constants import POSTS_PER_PAGE
from .forms import PostForm, CommentForm
from .models import Group, Post, User
from .utils import pagi
from django.views.decorators.cache import cache_page


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_list.html'
    post_list = group.posts.all()
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


@cache_page(20)
def index(request):
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    post_list = Post.objects.all()
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
    post_list = author.author_posts.all()
    title = 'Профайл пользователя'
    context = {
        'title': title,
        'page_obj': pagi(request, post_list, POSTS_PER_PAGE),
        'author': author,
        'posts_count': post_list.count(),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    posts_count = Post.objects.filter(author=post.author).count()
    comments = post.comments.all()
    # new_comment = None
    if request.method == 'POST':
        form = post_create(data=request.POST)
    else:
        form = CommentForm()
    context = {
        'post': post,
        'posts_count': posts_count,
        'comments': comments,
        'form': form,
    }
    return render(request, template, context)


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
    form = PostForm(
        request.POST or None,
        files=request.FILES or None)
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
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    if request.method == 'POST':
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
            instance=post,
        )
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.text = form.cleaned_data['text']
            post.group = form.cleaned_data['group']
            post.image = form.cleaned_data['image']
            post.save()
            return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(instance=post,)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.text = form.cleaned_data['text']
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)
