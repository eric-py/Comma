from django.forms import ClearableFileInput
from django.utils.html import format_html

class CustomClearableFileInput(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return format_html(
            '<input type="file" name="{}" class="hidden" id="{}">'
            '{}',
            name,
            attrs['id'],
            self.clear_checkbox_html(context) if value and hasattr(value, 'url') else '',
        )

    def clear_checkbox_html(self, context):
        return format_html(
            '<div class="my-4"><label for="{}-clear_id" class="inline-flex items-center">'
            '<input type="checkbox" name="{}-clear" id="{}-clear_id" class="form-checkbox h-5 w-5 text-pink-600">'
            '<span class="mr-2 text-gray-700">پاک کردن تصویر پروفایل</span></label></div>',
            context['widget']['attrs']['id'],
            context['widget']['name'],
            context['widget']['attrs']['id'],
        )