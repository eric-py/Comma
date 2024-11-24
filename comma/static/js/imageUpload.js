document.addEventListener('DOMContentLoaded', function() {
    const fileUpload = document.getElementById('file-upload');
    const imagePreview = document.getElementById('image-preview');
    const preview = document.getElementById('preview');
    const uploadIcon = document.getElementById('upload-icon');
    const removeButton = document.getElementById('remove-images');

    function showPreview(src) {
        imagePreview.src = src;
        preview.classList.remove('hidden');
        preview.classList.add('block');
        uploadIcon.classList.add('hidden');
    }

    function hidePreview() {
        preview.classList.add('hidden');
        preview.classList.remove('block');
        uploadIcon.classList.remove('hidden');
        fileUpload.value = '';
    }

    if (imagePreview.src && imagePreview.src !== window.location.href) {
        showPreview(imagePreview.src);
    }

    fileUpload.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                showPreview(e.target.result);
            };
            reader.readAsDataURL(file);
        }
    });

    removeButton.addEventListener('click', function(event) {
        event.preventDefault();
        hidePreview();
    });
});