document.addEventListener('DOMContentLoaded', function() {
    const saveButtons = document.querySelectorAll('.save-button');

    saveButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.closest('.bg-white').querySelector('.like-button').dataset.postId;
            const icon = this.querySelector('i');

            fetch(`/post/${postId}/save/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.saved) {
                    icon.classList.replace('far', 'fas');
                    icon.classList.add('text-cyan-400');
                } else {
                    icon.classList.replace('fas', 'far');
                    icon.classList.remove('text-cyan-400');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}