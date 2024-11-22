document.addEventListener('DOMContentLoaded', function() {
    const fileUpload = document.getElementById('file-upload');
    const preview = document.getElementById('preview');
    const imagePreview = document.getElementById('image-preview');
    const uploadIcon = document.getElementById('upload-icon');
    const removeButton = document.getElementById('remove-image');

    fileUpload.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                preview.classList.remove('hidden');
                uploadIcon.classList.add('hidden');
            }
            reader.readAsDataURL(file);
        }
    });

    removeButton.addEventListener('click', function() {
        imagePreview.src = '#';
        preview.classList.add('hidden');
        uploadIcon.classList.remove('hidden');
        fileUpload.value = '';
    });

    const dropZone = document.querySelector('.border-dashed');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropZone.classList.add('border-pink-500', 'dark:border-pink-400');
    }

    function unhighlight() {
        dropZone.classList.remove('border-pink-500', 'dark:border-pink-400');
    }

    dropZone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const file = dt.files[0];

        if (file && file.type.startsWith('image/')) {
            fileUpload.files = dt.files;
            const event = new Event('change');
            fileUpload.dispatchEvent(event);
        }
    }
});