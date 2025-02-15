document.addEventListener("DOMContentLoaded", () => {
    // Handle clicking on posts (for future features)
    const posts = document.querySelectorAll(".post");
    posts.forEach(post => {
        post.addEventListener("click", () => {
            alert("You clicked on a post by " + post.querySelector("strong").innerText);
        });
    });

    // Handle messaging form submission
    const messageForm = document.querySelector(".message-form");
    if (messageForm) {
        messageForm.addEventListener("submit", (event) => {
            event.preventDefault();
            const messageInput = document.querySelector(".message-form input");
            const chatBox = document.querySelector(".chat-box");

            const message = messageInput.value.trim();
            if (message) {
                const newMessage = document.createElement("p");
                newMessage.innerHTML = `<strong>You:</strong> ${message}`;
                chatBox.appendChild(newMessage);
                chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to latest message
                messageInput.value = "";
            }
        });
    }
});
