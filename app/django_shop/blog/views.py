from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.views.generic import View


# Create your views here.


def posts_list(request):

    # get all posts
    posts = Post.objects.all()

    # break all posts to 10 posts on page with Paginator
    paginator = Paginator(posts, 10)

    # request current page and take it from paginator object
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    context = {
        'page': page,
    }
    return render(request, 'blog/posts_list.html', context=context)


class PostDetail(View):
    def get(self, request, slug):

        # request post by slug
        post = get_object_or_404(Post, slug=slug)
        return render(request, 'blog/post_detail.html', context={'post': post})

class TagList(View):
    def get(self, request, slug):

        # get tag by slug and get all posts by tag
        tag = get_object_or_404(Tag, slug=slug)
        return render(request, 'blog/tag_list.html', context={'tag': tag})
