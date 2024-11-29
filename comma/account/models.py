from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from extensions.utils import validate_image, user_directory_path, convert_date_to_jalali

from posts.models import Post, Comment

from PIL import Image

# Create your models here.

class UserConnection(models.Model):
    follower = models.ForeignKey('User', related_name='following', on_delete=models.CASCADE, verbose_name='فالوور')
    following = models.ForeignKey('User', related_name='followers', on_delete=models.CASCADE, verbose_name='فالووینگ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'ارتباط کاربری'
        verbose_name_plural = 'ارتباطات کاربری'

    def __str__(self):
        return f"دنبال کردن {self.following.username} توسط {self.follower.username} در {self.jdate_joined()}"

    def jdate_joined(self):
        return convert_date_to_jalali(self.created_at, time=True)
    jdate_joined.short_description = 'تاریخ فالو کردن'

class FollowRequest(models.Model):
    from_user = models.ForeignKey('User', related_name='sent_follow_requests', on_delete=models.CASCADE, verbose_name='از یوزر')
    to_user = models.ForeignKey('User', related_name='received_follow_requests', on_delete=models.CASCADE, verbose_name='به یوزر')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
        verbose_name = 'درخواست فالو'
        verbose_name_plural = 'درخواست‌های فالو'
    
    def __str__(self):
        return f"درخواست از {self.from_user.username} به {self.to_user.username} در {self.jdate_joined()}"

    def jdate_joined(self):
        return convert_date_to_jalali(self.created_at, time=True)
    jdate_joined.short_description = 'تاریخ درخواست'

class User(AbstractUser):
    email = models.EmailField('ایمیل', unique=True)
    bio = models.TextField('بیوگرافی', blank=True, null=True, max_length=200)
    is_private = models.BooleanField('حساب خصوصی', default=False)
    profile_pics = models.ImageField('تصویر پروفایل',upload_to=user_directory_path,blank=True,null=True,validators=[validate_image])

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
    
    def __str__(self):
        return self.username

    def jdate_joined(self):
        return convert_date_to_jalali(self.date_joined, time=True)
    jdate_joined.short_description = 'تاریخ عضویت'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_pics:
            self._process_profile_picture()

    def _process_profile_picture(self):
        with Image.open(self.profile_pics.path) as img:
            if img.height != img.width:
                min_size = min(img.height, img.width)
                left = (img.width - min_size) // 2
                top = (img.height - min_size) // 2
                right = left + min_size
                bottom = top + min_size
                img = img.crop((left, top, right, bottom))
            
            img = img.resize((100, 100), Image.LANCZOS)
            img.save(self.profile_pics.path)

class Activity(models.Model):
    ACTIVITY_TYPES = (
        ('follow', 'فالو'),
        ('follow_request', 'درخواست فالو'),
        ('like', 'لایک'),
        ('comment_like', 'لایک کامنت'),
        ('comment', 'کامنت'),
        ('reply', 'ریپلای'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities', verbose_name='کاربر')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES, verbose_name='نوع فعالیت')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actions', verbose_name='فعالیت کننده')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, verbose_name='پست')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, verbose_name='کامنت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ فعالیت'  )
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده'  )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'فعالیت'
        verbose_name_plural = 'فعالیت‌ها'

    def __str__(self):
        return f"{self.actor.username} {self.get_activity_type_display()} در {self.created_at}"

    def jcreated_at(self):
        return convert_date_to_jalali(self.created_at, time=True)
    jcreated_at.short_description = 'تاریخ فعالیت'

    @classmethod
    def create_activity(cls, user, activity_type, actor, post=None, comment=None):
        return cls.objects.create(
            user=user,
            activity_type=activity_type,
            actor=actor,
            post=post,
            comment=comment
        )