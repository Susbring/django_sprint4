"""View-функции"""
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.http import Http404
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy

from blog.forms import CreateForm, CommentForm, ProfileForm
from blog.models import Post, Category, Comment
from .querysets import apply_publication_filters, apply_publication_annotat
from .utils import paginated_page_object
from .constants import NUMBER_OF_RECORDS_ON_THE_PAGE


User = get_user_model()


def index(request):
    """Главная страница."""
    template_name = 'blog/index.html'
    post_list = Post.objects.select_related(
        'category',
        'author',
    ).order_by('-pub_date')
    post_list = apply_publication_annotat(apply_publication_filters(post_list))
    page_obj = paginated_page_object(
        post_list,
        request,
        NUMBER_OF_RECORDS_ON_THE_PAGE)
    context = {
        'page_obj': page_obj
    }
    return render(request, template_name, context)


class PostDetailView(DetailView):
    """CBV функция страницы поста"""

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_object(self):
        object = super(PostDetailView, self).get_object()
        if self.request.user != object.author and (
            not object.is_published or not object.category.is_published
        ):
            raise Http404()
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


def category_posts(request, category_slug):
    """Страница с категорией поста."""
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = apply_publication_filters(
        category.posts.select_related('location', 'author')
        )
    page_obj = paginated_page_object(
        post_list,
        request,
        NUMBER_OF_RECORDS_ON_THE_PAGE)
    context = {'category': category,
               'page_obj': page_obj}
    return render(request, template_name, context)


def profile(request, username):
    """Вью функция профиля пользователя"""
    profile = get_object_or_404(User, username=username)
    post_list = apply_publication_annotat(
        profile.posts.all())
    page_obj = paginated_page_object(
        post_list,
        request,
        NUMBER_OF_RECORDS_ON_THE_PAGE)
    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    """CBV функция создания поста"""

    model = Post
    form_class = CreateForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """CBV функция редактирования профиля"""

    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostEditView(LoginRequiredMixin, UpdateView):
    """CBV функция редактирования поста"""

    model = Post
    form_class = CreateForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


@login_required
def delete_post(request, post_id):
    """Вью функция удаления поста"""
    template_name = 'blog/create.html'
    instance = get_object_or_404(
        Post,
        pk=post_id,
        author__username=request.user
    )
    form = CreateForm(instance=instance)
    context = {'form': form}
    if (request.method == 'POST'
       and instance.author == request.user):
        instance.delete()
        return redirect('blog:profile', request.user)

    context = {
        'post': instance,
    }
    return render(request, template_name, context)


@login_required
def add_comment(request, post_id):
    """Вью функция добавления комментария"""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Вью функция редактирования комментария"""
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden(
            'У вас нет прав для редактирования этого комментария.'
        )

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id)
    form = CommentForm(instance=comment)
    context = {
        'form': form,
        'comment': comment,
    }
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    """Вью функция удаления комментария"""
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden(
            'У вас нет прав для удаления этого комментария.'
        )

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id)

    context = {
        'comment': comment,
    }
    return render(request, 'blog/comment.html', context)
