document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    if (chatBox) {
        const chatId = chatBox.getAttribute("data-chat-id");
        // Poll every second (1000 milliseconds)
        setInterval(() => {
            fetch(`/api/get_chat_messages/?chat_id=${chatId}`)
                .then(response => response.json())
                .then(data => {
                    // Clear the chat box
                    chatBox.innerHTML = "";
                    data.messages.forEach(msg => {
                        // Create a container div for the message
                        const msgContainer = document.createElement("div");
                        msgContainer.classList.add("mb-3", "d-flex");
                        
                        // Determine if the message is sent by current user
                        if (msg.sender === currentUser) {
                            msgContainer.classList.add("justify-content-end", "message-right");
                        } else {
                            msgContainer.classList.add("justify-content-start", "message-left");
                        }
                        
                        // Create inner div for styling the message box
                        const msgBox = document.createElement("div");
                        msgBox.classList.add("message-box");
                        msgBox.innerHTML = `
                            <small><strong>${msg.sender}</strong></small>
                            <p class="mb-0">${msg.content}</p>
                            <small class="text-muted">${msg.timestamp}</small>
                        `;
                        msgContainer.appendChild(msgBox);
                        chatBox.appendChild(msgContainer);
                    });
                    // Auto-scroll to bottom
                    chatBox.scrollTop = chatBox.scrollHeight;
                })
                .catch(error => console.error("Error fetching messages:", error));
        }, 1000);
    }
});
