document.addEventListener('DOMContentLoaded', function() {
    const showPostsBtn = document.getElementById('showPosts');
    const showSavedBtn = document.getElementById('showSaved');
    const postsGrid = document.getElementById('postsGrid');
    const savedGrid = document.getElementById('savedGrid');

    showPostsBtn.addEventListener('click', function() {
        postsGrid.classList.remove('hidden');
        savedGrid.classList.add('hidden');
        showPostsBtn.classList.replace('bg-gray-300', 'bg-pink-500');
        showPostsBtn.classList.replace('text-gray-700', 'text-white');
        showSavedBtn.classList.replace('bg-pink-500', 'bg-gray-300');
        showSavedBtn.classList.replace('text-white', 'text-gray-700');
    });

    showSavedBtn.addEventListener('click', function() {
        postsGrid.classList.add('hidden');
        savedGrid.classList.remove('hidden');
        showSavedBtn.classList.replace('bg-gray-300', 'bg-pink-500');
        showSavedBtn.classList.replace('text-gray-700', 'text-white');
        showPostsBtn.classList.replace('bg-pink-500', 'bg-gray-300');
        showPostsBtn.classList.replace('text-white', 'text-gray-700');
    });
});