document.addEventListener('DOMContentLoaded', function() {
    const postOptionsButton = document.getElementById('postOptionsButton');
    const postOptions = document.getElementById('postOptions');

    postOptionsButton.addEventListener('click', (event) => {
        event.stopPropagation();
        postOptions.classList.toggle('hidden');
    });

    document.addEventListener('click', () => {
        postOptions.classList.add('hidden');
    });

    const sendModal = document.getElementById('sendModal');
    const closeSendModal = document.getElementById('closeSendModal');
    const sendButtons = document.querySelectorAll('.send-button');
    const userList = document.getElementById('userList');
    const sendButton = document.getElementById('sendButton');

    const users = [
        { id: 1, name: 'کاربر ۱' },
        { id: 2, name: 'کاربر ۲' },
        { id: 3, name: 'کاربر ۳' },
        { id: 4, name: 'کاربر ۴' },
        { id: 5, name: 'کاربر ۵' },
    ];

    users.forEach(user => {
        const userElement = document.createElement('div');
        userElement.classList.add('flex', 'items-center', 'p-2', 'hover:bg-gray-100', 'dark:hover:bg-gray-700', 'cursor-pointer', 'rounded');
        userElement.innerHTML = `
            <img src="https://via.placeholder.com/32" alt="${user.name}" class="w-8 h-8 rounded-full ml-2">
            <span>${user.name}</span>
        `;
        userElement.setAttribute('data-user-id', user.id);
        userList.appendChild(userElement);
    });

    sendButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            sendModal.classList.remove('hidden');
            sendModal.classList.add('flex');
        });
    });

    closeSendModal.addEventListener('click', function() {
        sendModal.classList.add('hidden');
        sendModal.classList.remove('flex');
    });

    let selectedUsers = new Set();
    userList.addEventListener('click', function(e) {
        const userElement = e.target.closest('[data-user-id]');
        if (userElement) {
            const userId = userElement.getAttribute('data-user-id');
            if (selectedUsers.has(userId)) {
                selectedUsers.delete(userId);
                userElement.classList.remove('bg-pink-100', 'dark:bg-pink-800');
            } else {
                selectedUsers.add(userId);
                userElement.classList.add('bg-pink-100', 'dark:bg-pink-800');
            }
            sendButton.disabled = selectedUsers.size === 0;
        }
    });

    sendButton.addEventListener('click', function() {
        console.log('ارسال به کاربران:', Array.from(selectedUsers));
        sendModal.classList.add('hidden');
        sendModal.classList.remove('flex');
        selectedUsers.clear();
        userList.querySelectorAll('.bg-pink-100, .dark:bg-pink-800').forEach(el => {
            el.classList.remove('bg-pink-100', 'dark:bg-pink-800');
        });
        sendButton.disabled = true;
    });

    sendModal.addEventListener('click', function(e) {
        if (e.target === sendModal) {
            sendModal.classList.add('hidden');
            sendModal.classList.remove('flex');
        }
    });


});
