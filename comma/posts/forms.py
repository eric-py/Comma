from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError("حجم تصویر نباید بیشتر از 10 مگابایت باشد.")
            return image
        else:
            raise forms.ValidationError("لطفاً یک تصویر انتخاب کنید.")