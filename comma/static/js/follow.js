document.addEventListener('DOMContentLoaded', function() {
    const followButton = document.getElementById('followButton');
    if (followButton) {
        followButton.addEventListener('click', function() {
            const username = this.dataset.username;
            const currentState = this.textContent.trim();

            fetch(`/account/${username}/follow/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    if (currentState === 'فالو کردن') {
                        this.textContent = data.is_private ? 'لغو درخواست' : 'آنفالو کردن';
                    } else if (currentState === 'آنفالو کردن') {
                        this.textContent = data.is_private ? 'درخواست فالو' : 'فالو کردن';
                    } else if (currentState === 'لغو درخواست') {
                        this.textContent = 'درخواست فالو';
                    } else if (currentState === 'درخواست فالو') {
                        this.textContent = 'لغو درخواست';
                    }
                }
            });
        });
    }
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