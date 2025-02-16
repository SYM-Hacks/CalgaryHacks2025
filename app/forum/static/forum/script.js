document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    if (!chatBox) return;  // If no chat box on page, exit

    const chatId = chatBox.getAttribute("data-chat-id");
    let pausedUpdates = false;
    const BOTTOM_TOLERANCE = 5;

    // Check if scrolled near bottom
    function isAtBottom() {
        return Math.abs(chatBox.scrollHeight - chatBox.clientHeight - chatBox.scrollTop) < BOTTOM_TOLERANCE;
    }

    // Pause updates if user scrolls away from bottom
    chatBox.addEventListener("scroll", () => {
        if (!isAtBottom()) {
            pausedUpdates = true;
        } else {
            // Once user scrolls back to bottom, resume updates and refresh immediately
            if (pausedUpdates) {
                pausedUpdates = false;
                loadMessages();
            }
        }
    });

    // Rebuild entire chat from data
    function rebuildChat(messages) {
        const wasAtBottom = isAtBottom();
        chatBox.innerHTML = "";

        messages.forEach(msg => {
            const msgContainer = document.createElement("div");
            msgContainer.classList.add("mb-3", "d-flex");

            // Align left or right
            if (msg.sender === currentUser) {
                msgContainer.classList.add("justify-content-end", "message-right");
            } else {
                msgContainer.classList.add("justify-content-start", "message-left");
            }

            const msgBox = document.createElement("div");
            msgBox.classList.add("message-box");

            // "Discord-like": image first, then text, then small sender/timestamp
            let innerHTML = "";

            // If there's an image, display it first
            if (msg.image) {
                innerHTML += `<img src="${msg.image}" alt="Message Image" class="message-image">`;
            }

            // Then the text content if present
            if (msg.content) {
                innerHTML += `<p class="mb-2">${msg.content}</p>`;
            }

            // Finally, the sender and timestamp at the bottom
            innerHTML += `
                <small><strong>${msg.sender}</strong> · ${msg.timestamp}</small>
            `;

            msgBox.innerHTML = innerHTML;
            msgContainer.appendChild(msgBox);
            chatBox.appendChild(msgContainer);
        });

        // If we were at bottom, scroll down again
        if (wasAtBottom) {
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // Fetch messages from server
    function loadMessages() {
        fetch(`/api/get_chat_messages/?chat_id=${chatId}`)
            .then(response => response.json())
            .then(data => {
                // If not paused, rebuild
                if (!pausedUpdates) {
                    rebuildChat(data.messages);
                }
            })
            .catch(error => console.error("Error fetching messages:", error));
    }

    // Poll server every 3 seconds for new messages
    setInterval(() => {
        if (!pausedUpdates) {
            loadMessages();
        }
    }, 1000);

    // Initial load
    loadMessages();
});
