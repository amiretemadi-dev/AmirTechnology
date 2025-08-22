from django.db import models
from django.template.defaultfilters import slugify
from account.models import CustomUser
from django_prose_editor.fields import ProseEditorField
from django.utils.html import format_html, mark_safe
from django.urls import reverse_lazy


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def short_date(self):
        return self.created_at.strftime('%b %d, %Y')

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    main_topic = models.CharField(max_length=20)
    title = models.CharField(max_length=150, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='posts')
    body = ProseEditorField(
        extensions={
            "Bold": True,
            "Italic": True,
            "Strike": True,
            "Underline": True,
            "HardBreak": True,
            "Heading": {
                "levels": [1, 2, 3]
            },
            "BulletList": True,
            "OrderedList": True,
            "Blockquote": True,
            "Link": {
                "enableTarget": True,
                "protocols": ["http", "https", "mailto"],
            },
            "Table": True,
            "History": True,
            "HTML": True,
            "Typographic": True,
        },
        sanitize=True
    )

    objects = models.Manager()

    summary = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_time = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=150, unique=True, help_text='please do not change this field Thank you.')
    image = models.ImageField(upload_to="images/posts", null=True, blank=True)
    status = models.BooleanField(default=False)

    def preview_image(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="max-height: 250px;" />')

    def display_image(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" style="max-height: 50px;" />')
        return format_html('<span style="color:red;text-align: center;">no image</span>')

    def __str__(self):
        return f'{self.main_topic} - {self.title}'

    def short_date(self):
        return self.created_at.strftime('%b %d, %Y')

    def get_absolute_url(self):
        return reverse_lazy('post:detail', kwargs={'slug': self.slug})


class Like(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.author.username}-{self.post.title}'

class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    objects = models.Manager()
    def __str__(self):
        return f'from {self.author.username}-to-{self.post.title}-post'

class Contact(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contacts')
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()

    def __str__(self):
        return f'{self.author.username}-{self.subject}'