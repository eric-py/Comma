document.addEventListener('DOMContentLoaded', function() {
    const followButton = document.getElementById('followButton');
    
    if (followButton) {
        followButton.addEventListener('click', function() {
            const action = this.dataset.action;
            const username = this.dataset.username;
            let url;

            switch(action) {
                case 'follow':
                case 'sendrequest':
                    url = `/account/${username}/follow/`;
                    break;
                case 'unfollow':
                    url = `/account/${username}/unfollow/`;
                    break;
                case 'reject':
                    url = `/account/${username}/reject_request/`;
                    break;
                case 'accept':
                    url = `/account/${username}/accept_request/`;
                    break;
                default:
                    console.error('Unknown action');
                    return;
            }

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateButtonState(data.action);
                } else {
                    console.error('Error:', data.message);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
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

function updateButtonState(action, isPrivate) {
    const button = document.getElementById('followButton');
    
    switch(action) {
        case 'followed':
            button.textContent = 'آنفالو کردن';
            button.dataset.action = 'unfollow';
            button.classList.remove('bg-pink-500', 'hover:bg-pink-600');
            button.classList.add('bg-gray-500', 'hover:bg-gray-600');
            break;
        case 'unfollowed':
            if (isPrivate) {
                button.textContent = 'درخواست فالو';
                button.dataset.action = 'sendrequest';
            } else {
                button.textContent = 'فالو کردن';
                button.dataset.action = 'follow';
            }
            button.classList.remove('bg-gray-500', 'hover:bg-gray-600');
            button.classList.add('bg-pink-500', 'hover:bg-pink-600');
            break;
        case 'request_sent':
            button.textContent = 'لغو درخواست';
            button.dataset.action = 'reject';
            button.classList.remove('bg-pink-500', 'hover:bg-pink-600');
            button.classList.add('bg-gray-500', 'hover:bg-gray-600');
            break;
        case 'request_cancelled':
            button.textContent = 'درخواست فالو';
            button.dataset.action = 'sendrequest';
            button.classList.remove('bg-gray-500', 'hover:bg-gray-600');
            button.classList.add('bg-pink-500', 'hover:bg-pink-600');
            break;
        case 'request_accepted':
            button.textContent = 'آنفالو کردن';
            button.dataset.action = 'unfollow';
            button.classList.remove('bg-pink-500', 'hover:bg-pink-600');
            button.classList.add('bg-gray-500', 'hover:bg-gray-600');
            break;
    }
}