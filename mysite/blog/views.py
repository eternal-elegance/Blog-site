from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin  # 11
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

# Create your views here.

# Post Views
class AboutView(TemplateView):
    """ THIS IS ABOUT VIEW """

    template_name = "about.html"


class PostListView(ListView):
    """ THIS IS HOME PAGE VIEW """

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by(
            "-published_date"
        )
        # 10


class PostDetailView(DetailView):
    """ THIS IS INSIDE POST VIEW """

    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    """ THIS IS CREATE VIEW """

    login_url = "/login/"
    redirect_field_name = "blog/post_detail.html"
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """ THIS IS UPDATE VIEW """

    login_url = "/login/"
    redirect_field_name = "blog/post_detail.html"
    form_class = PostForm
    model = Post
    # 12


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """ This is Delete View """

    model = Post
    success_url = reverse_lazy("post_list")


##############################################################################################
############################# SOME EXTRA POST STUFF  #########################################
##############################################################################################


# Drafts View
class DraftListView(LoginRequiredMixin, ListView):
    """ THIS IS THE DRAFT VIEW """

    context_object_name = "draft_list"
    login_url = "/login/"
    redirect_field_name = "blog/post_draft_list.html"
    model = Post
    template_name = "post_draft_list.html"

    def get_queryset(self):
        """ Getting objects which don't have published date """
        # posts are comming from here
        return Post.objects.filter(published_date__isnull=True).order_by("created_date")


@login_required
def post_publish(request, pk):
    """ This is the post publish view """

    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect("post_detail", pk=pk)


############################################################################################
################################################COMMENTS####################################
############################################################################################


@login_required  # 13
def add_comment_to_post(request, pk):
    """ This is the comments view """

    post = get_object_or_404(Post, pk=pk)  # 14
    if request.method == "POST":
        form = CommentForm(request.POST)  # 15
        if form.is_valid():
            comment = form.save(commit=False)  # 16
            comment.post = post  # 17
            comment.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = CommentForm()  # 18
    return render(request, "blog/comment_form.html", {"form": form})


@login_required
def comment_approve(request, pk):
    """ This is to approve a comment """
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()  # 19
    return redirect("post_detail", pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    """ This is to remove a comment """
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect("post_detail", pk=post_pk)
