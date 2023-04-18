from django.shortcuts import render, redirect
from .models import Post
from django.views.generic import ListView
from django.views import View
from .forms import CommentForm

# Create your views here.

# helper function for sort


# home page contains latest 3 post
class HomePageView(ListView):
    template_name = 'blog/home.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        query_set = super().get_queryset()
        data = query_set[:3]
        return data


class IndexPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ['-date']
    context_object_name = 'all_posts'


class ShowPageView(View):
    # helper function
    def is_saved(self, request, post_id):
        stored_posts = request.session.get('stored_posts')
        if stored_posts:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by('-id'),
            "is_saved_for_later":self.is_saved(request,post.id)
        }
        return render(request, 'blog/show.html', context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(request.path)

        context = {
            "post": post,
            "tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by('-id'),
            "is_saved_for_later":self.is_saved(request,post.id)
        }
        return render(request, 'blog/show.html', context)


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get('stored_posts')
        context = {}
        if not stored_posts or len(stored_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            context['posts'] = Post.objects.filter(id__in=stored_posts)
            context['has_posts'] = True
        return render(request, 'blog/read-later.html', context)

    def post(self, request):
        stored_posts = request.session.get('stored_posts')
        if not stored_posts:
            stored_posts = []
        post_id = int(request.POST.get('post_id'))

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
      
        request.session['stored_posts'] = stored_posts
        return redirect('/')
