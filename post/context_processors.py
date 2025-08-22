from .models import Post


def three_random_post(request):
    posts = Post.objects.order_by('?')[0:3]
    return {'random_posts': posts}