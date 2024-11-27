document.addEventListener('DOMContentLoaded', function() {
    const replyButtons = document.querySelectorAll('.reply-btn');
    replyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.dataset.commentId;
            const replyForm = document.getElementById(`reply-form-${commentId}`);
            replyForm.classList.toggle('hidden');
        });
    });

    const commentForms = document.querySelectorAll('form');
    commentForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const isReply = this.id !== 'mainCommentForm';
            const url = isReply ? '/post/' + postId + '/add_reply/' : '/post/' + postId + '/add_comment/';

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const newComment = createCommentElement(data);

                    if (isReply) {
                        const parentCommentId = this.querySelector('input[name="parent_id"]').value;
                        const parentComment = document.getElementById(`comment-${parentCommentId}`);
                        if (parentComment) {
                            const repliesContainer = parentComment.querySelector('.replies-container');
                            if (repliesContainer) {
                                repliesContainer.appendChild(newComment);
                            } else {
                                const newRepliesContainer = document.createElement('div');
                                newRepliesContainer.className = 'replies-container mt-2 ml-8';
                                newRepliesContainer.appendChild(newComment);
                                parentComment.appendChild(newRepliesContainer);
                            }
                        }
                    } else {
                        document.getElementById('commentsList').prepend(newComment);
                    }

                    this.reset();
                } else {
                    console.error('خطا در ارسال کامنت:', data.message);
                }
            })
            .catch(error => {
                console.error('خطا در ارسال درخواست:', error);
            });
        });
    });

    $(document).on('click', '.like-comment-btn', function(e) {
        e.preventDefault();
        var $this = $(this);
        var commentId = $this.data('comment-id');
        $.ajax({
            url: '/comment/' + commentId + '/like/',
            type: 'POST',
            headers: {'X-CSRFToken': csrfToken},
            success: function(data) {
                if (data.status === 'success') {
                    var $icon = $this.find('i');
                    var $likesCount = $this.find('.comment-likes-count');
                    
                    $likesCount.text(data.likes_count);
                    
                    if (data.liked) {
                        $icon.removeClass('far').addClass('fas text-pink-500');
                    } else {
                        $icon.removeClass('fas text-pink-500').addClass('far');
                    }
                }
            },
            error: function(xhr, status, error) {
                console.error("Error liking comment:", error);
            }
        });
    });
});

function createCommentElement(data) {
    const newComment = document.createElement('div');
    newComment.className = 'comment-container bg-white dark:bg-gray-800 p-4 rounded-lg shadow mt-4';
    newComment.innerHTML = `
        <div class="flex items-start space-x-3 space-x-reverse">
            <img src="${data.user_profile_pic}" alt="تصویر پروفایل" class="w-8 h-8 rounded-full">
            <div class="flex-grow">
                <div class="flex justify-between items-start">
                    <p class="text-sm my-1">
                        <a href="/account/profile/${data.username}/" class="font-semibold hover:underline">${data.username}</a>
                        ${data.text}
                    </p>
                </div>
                <p class="text-xs text-gray-500">${data.created_at}</p>
            </div>
        </div>
    `;
    return newComment;
}