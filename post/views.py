from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View, CreateView
from post.forms import ContactForm
from post.models import Post, Category, Like, Comment, Contact
from django.urls import reverse_lazy


class PostListView(ListView):
    model = Post
    paginate_by = 2
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_slug'] = self.request.GET.get('category_slug')
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('account:login')
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_post'] = Post.objects.filter(main_topic__icontains=self.object.main_topic).exclude(id=self.object.id).order_by('?')[0:3]
        context['categories'] = Category.objects.all().annotate(num_posts=Count('posts'))
        context['is_liked'] = Like.objects.filter(post=self.object, author_id=self.request.user.id).exists()
        return context

    def post(self, request, *args, **kwargs):
        parent_id = request.POST.get('parent_id')
        content = request.POST.get('text')

        parent_comment = None
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
            except:
                parent_comment = None

        comment= Comment.objects.create(post=self.get_object(), content=content, author=request.user, parent_id=parent_comment)

        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'username': comment.author.username,
            'text': comment.content,
            'parent_id': parent_comment.id if parent_comment else None
        })


class LikeView(LoginRequiredMixin, View):
    login_url = reverse_lazy('account:login')

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        like = Like.objects.filter(post=post, author=request.user)

        if like.exists():
            like.delete()
            liked = False
        else:
            Like.objects.create(post=post, author=request.user)
            liked = True

        return JsonResponse({'liked': liked})

class ContactUsView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('account:login')
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('home:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.email = self.request.user.email
        return super().form_valid(form)

