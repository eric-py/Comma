from d2j import D2J
from datetime import datetime
import uuid

from django.core.exceptions import ValidationError

def convert_date_to_jalali(date, time=True):
    d2j_converter = D2J(date.strftime("%Y/%m/%d"))
    result = d2j_converter.as_verbose()
    if time:
        result = f"{result} ساعت: {date.strftime('%H:%M')}"
    return result

def validate_image(image):
    if image.size > 1024 * 1024 * 10:  # 10MB
        return False
    if image.width > 2000 or image.height > 2000:
        return False
    return True

def user_directory_path(instance, filename):
    if hasattr(instance, 'username'):
        folder = 'profile_pics'
        user_id = instance.id
    else:
        folder = 'posts'
        user_id = instance.user.id if instance.user else 'unknown'
    
    random_string = uuid.uuid4().hex[:8]
    name, extension = filename.rsplit('.', 1)
    new_filename = f"{name}_{random_string}.{extension}"
    return f'user_{user_id}/{folder}/{new_filename}'

def create_comment_or_reply(post, user, content, parent=None):
    
    from posts.models import Comment
    
    if len(content) > 200:
        raise ValidationError('متن کامنت نباید بیشتر از 200 کاراکتر باشد.')
    
    comment = Comment.objects.create(
        post=post,
        user=user,
        text=content,
        parent=parent
    )
    comment.full_clean()
    return comment