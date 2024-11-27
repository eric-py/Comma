from django.db import models
from django.conf import settings
from django.db.models import Q

from extensions.utils import convert_date_to_jalali, validate_image, user_directory_path

from PIL import Image

# Managers
class PostManager(models.Manager):
    def posts(self, user):
        return self.filter(
            Q(user=user) | Q(user__in=user.following.values('following'))
        ).distinct().order_by('-created_at')

class SavedPostManager(models.Manager):
    def saved_posts(self, user):
        saved_posts = self.filter(user=user)
        visible_posts = []
        
        for saved_post in saved_posts:
            post_owner = saved_post.post.user
            if post_owner == user:
                visible_posts.append(saved_post.post)
            elif not post_owner.is_private:
                visible_posts.append(saved_post.post)
            elif user.following.filter(following=post_owner).exists():
                visible_posts.append(saved_post.post)
        
        return Post.objects.filter(id__in=[post.id for post in visible_posts]).order_by('-created_at')

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', verbose_name='کاربر')
    image = models.ImageField(upload_to=user_directory_path, verbose_name='تصویر', validators=[validate_image])
    caption = models.TextField(blank=True, verbose_name='کپشن', null=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')

    objects = PostManager()

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"پست توسط {self.user.username} در {self.jcreated_at()}"

    def jcreated_at(self):
        return convert_date_to_jalali(self.created_at, time=True)
    jcreated_at.short_description = 'ایجاد شده در'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self._process_image()

    def _process_image(self):
        with Image.open(self.image.path) as img:
            if img.height != img.width:
                min_size = min(img.height, img.width)
                left = (img.width - min_size) // 2
                top = (img.height - min_size) // 2
                right = left + min_size
                bottom = top + min_size
                img = img.crop((left, top, right, bottom))
            
            img = img.resize((1024, 1024), Image.LANCZOS)
            img.save(self.image.path)

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name='لایک‌ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')

    class Meta:
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک‌ها'
        unique_together = ('user', 'post')

    def __str__(self):
        return f"لایک توسط {self.user.username} در {self.jcreated_at()}"
    
    def jcreated_at(self):
        return convert_date_to_jalali(self.created_at, time=True)
    jcreated_at.short_description = 'ایجاد شده در'

class SavedPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saves', verbose_name='ذخیره‌ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ذخیره شده در')

    objects = SavedPostManager()
    
    class Meta:
        verbose_name = 'ذخیره'
        verbose_name_plural = 'ذخیره‌ شده‌ها'
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"ذخیره توسط {self.user.username} در {self.jcreated_at()}"

    def jcreated_at(self):
        return convert_date_to_jalali(self.created_at, time=True)
    jcreated_at.short_description = 'ذخیره شده در'
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name='کامنت والد')
    text = models.TextField(verbose_name='متن کامنت', max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CommentLike', related_name='liked_comments', verbose_name='لایک‌ها')

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت‌ها'
        ordering = ['-created_at']

    def __str__(self):
        if self.parent:
            return f"پاسخ به کامنت {self.parent.id} توسط {self.user.username} در {self.jcreated_at()}"
        return f"کامنت توسط {self.user.username} در {self.jcreated_at()}"
    
    def jcreated_at(self):
        return convert_date_to_jalali(self.created_at, time=True)
    jcreated_at.short_description = 'ایجاد شده در'

    @property
    def is_reply(self):
        return self.parent is not None

    def get_replies(self):
        return Comment.objects.filter(parent=self)

    def like_count(self):
        return self.likes.count()

    def is_liked_by(self, user):
        return self.likes.filter(id=user.id).exists()

class CommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes', verbose_name='کامنت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')

    class Meta:
        verbose_name = 'لایک کامنت'
        verbose_name_plural = 'لایک‌های کامنت'
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"لایک کامنت توسط {self.user.username} در {self.jcreated_at()}"
    
    def jcreated_at(self):
        return convert_date_to_jalali(self.created_at, time=True)
    jcreated_at.short_description = 'ایجاد شده در'