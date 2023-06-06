from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from blog.forms import CommentForm, PostForm, UserForm
from blog.models import Category, Comment, Post, User

COUNT_OF_POSTS = 10


def post_filter():
    return Post.objects.select_related(
        'category',
        'location',
        'author',
    ).filter(
        pub_date__lt=datetime.now(),
        is_published=True,
        category__is_published=True,
    )


def index(request):
    post_list = (
        post_filter()
        .order_by('-pub_date')
        .annotate(comment_count=Count('comments'))
    )
    paginator = Paginator(post_list, COUNT_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = get_object_or_404(
        post_filter(),
        id=id
    )
    context = {
        'post': post,
        'form': CommentForm(),
        'comments': Comment.objects.filter(post_id=id),
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(
            is_published=True,
            slug=category_slug,
        )
    )
    post_list = (
        category.posts.filter(
            is_published=True,
            pub_date__lt=datetime.now(),
        )
        .order_by('-pub_date')
        .annotate(comment_count=Count('comments'))
    )
    paginator = Paginator(post_list, COUNT_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, 'blog/category.html', context)


def profile(request, username):
    if request.user.username == username:
        queryset = Post.objects.select_related(
            'location', 'category', 'author'
        )
    else:
        queryset = post_filter()
    user = get_object_or_404(
        User.objects.prefetch_related(
            Prefetch(
                'posts',
                queryset
                .order_by('-pub_date')
                .annotate(comment_count=Count('comments'))
            ),
        ).filter(username=username)
    )
    post_list = user.posts.all()
    paginator = Paginator(post_list, COUNT_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'profile': user,
    }
    return render(request, 'blog/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_success_url(self):
        username = self.request.user
        return reverse(
            'blog:profile',
            kwargs={'username': username},
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.user
        return reverse(
            'blog:profile',
            kwargs={'username': username},
        )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', id=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'id': self.kwargs['pk']},
        )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', id=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        comment = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = comment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'id': self.kwargs['pk']},
        )


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        if comment.author != request.user:
            return redirect('blog:post_detail', comment.post_id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'id': self.kwargs['post_id']},
        )


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        if comment.author != request.user:
            return redirect('blog:post_detail', comment.post_id)
        return super().dispatch(request, *args, **kwargs)
