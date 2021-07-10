from django.http import request
from django.shortcuts import render, get_object_or_404, reverse, redirect
from . import models
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    UpdateView,
    CreateView,
    DeleteView,
    ListView,
    DetailView,
)
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Post, Comment


class AboutView(TemplateView):
    template_name = "about.html"


class PostListView(LoginRequiredMixin, ListView):
    login_url = "accounts/login/"
    model = models.Post

    def get_queryset(self):

        qs = super().get_queryset()
        return qs.filter(publish_date__lte=timezone.now()).order_by("-publish_date")


class PostDetailView(LoginRequiredMixin, DetailView):
    login_url = "accounts/login/"
    model = models.Post


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = "accounts/login/"
    redirect_field_name = "post_detail.html"
    form_class = PostForm
    model = models.Post
    # fields = ("title", "text")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        
        print(self.object.author)
        self.object.save()

        return super().form_valid(form)


class PostUpdateView(UpdateView, LoginRequiredMixin):
    login_url = "accounts/login/"
    redirect_field_name = "post_detail.html"
    template_name = "post_update.html"
    # fields = ("title", "text")
    form_class = PostForm
    model = models.Post


class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = models.Post
    success_url = reverse_lazy("post_list")


class DraftListView(LoginRequiredMixin, ListView):
    login_url = "accounts/login/"
    model = models.Post
    template_name = "post_draft_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(publish_date__isnull=True).order_by("create_date")


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Comment
    success_url = reverse_lazy("post-details")


@login_required(login_url="/accounts/login/")
def post_publish(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    post.publish()
    return redirect("post_detail", pk=pk)


@login_required(login_url="/accounts/login/")
def post_unpublish(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    post.unpublish()
    return redirect("post_list")


@login_required(login_url="/accounts/login/")
def add_comments_to_post(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    User = request.user
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = User
            comment.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = CommentForm()
    return render(request, "comment_form.html", {"form": form})


@login_required(login_url="/accounts/login/")
def comment_approve(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    comment.approve()
    return redirect("post_detail", pk=comment.post.pk)


@login_required(login_url="/accounts/login/")
def comment_remove(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect("post_detail", pk=post_pk)
