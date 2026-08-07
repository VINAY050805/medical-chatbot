/* ============================================
   Medical AI Assistant Chat
============================================ */

let chatContainer;
let questionInput;
let sendButton;
let typingIndicator;

/* ============================================
   Initialize
============================================ */

document.addEventListener("DOMContentLoaded", () => {

    chatContainer = document.getElementById("chatContainer");
    questionInput = document.getElementById("questionInput");
    sendButton = document.getElementById("sendBtn");
    typingIndicator = document.getElementById("typingIndicator");

    if (!chatContainer || !questionInput || !sendButton) {
        console.error("Chat elements not found.");
        return;
    }

    sendButton.addEventListener("click", sendMessage);

    questionInput.addEventListener("keydown", (e) => {

        if (e.key === "Enter" && !e.shiftKey) {

            e.preventDefault();

            sendMessage();

        }

    });

    questionInput.addEventListener("input", autoResize);

});

/* ============================================
   Send Message
============================================ */

async function sendMessage() {

    const question = questionInput.value.trim();

    if (!question) return;

    sendButton.disabled = true;

    removeWelcomeCard();

    addMessage(question, "user");

    questionInput.value = "";

    autoResize();

    showTyping();

    try {

        const response = await askQuestion(question);

        hideTyping();

        addMessage(
            response.answer,
            "ai",
            response.sources || []
        );

    }

    catch (error) {

        hideTyping();

        console.error(error);

        addMessage(
            error.message ||
            "Unable to contact the server.",
            "ai"
        );

    }

    finally {

        sendButton.disabled = false;

        questionInput.focus();

    }

}

/* ============================================
   Add Message
============================================ */

function addMessage(
    text,
    sender,
    sources = []
) {

    const wrapper = document.createElement("div");
    wrapper.className = `message ${sender}`;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.innerHTML =
        sender === "user"
            ? `<i class="fa-solid fa-user"></i>`
            : `<i class="fa-solid fa-robot"></i>`;

    const bubble = document.createElement("div");
    bubble.className = "message-content";
    bubble.innerHTML = renderMarkdown(text);

    if (sender === "ai" && sources.length > 0) {

        bubble.appendChild(renderSources(sources));

    }

    if (sender === "ai") {

        const copy = document.createElement("button");
        copy.className = "copy-btn";
        copy.innerHTML = `<i class="fa-solid fa-copy"></i> Copy`;
        copy.onclick = async () => {

            await navigator.clipboard.writeText(text);

            showToast("Copied");

        };

        bubble.appendChild(copy);

    }

    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
    chatContainer.appendChild(wrapper);
    scrollBottom();

}

function renderMarkdown(text) {

    const html = marked.parse(text || "");

    if (window.DOMPurify) {

        return DOMPurify.sanitize(html);

    }

    const div = document.createElement("div");
    div.textContent = text || "";
    return div.innerHTML;

}

function renderSources(sources) {

    const sourceBox = document.createElement("div");
    sourceBox.className = "sources";

    const heading = document.createElement("strong");
    heading.textContent = "Sources";

    const list = document.createElement("ul");

    sources.forEach(source => {

        const item = document.createElement("li");

        const icon = document.createElement("i");
        icon.className = "fa-solid fa-file-pdf";

        const label = document.createElement("span");
        label.textContent = `${source.source} (Page ${source.page})`;

        item.appendChild(icon);
        item.appendChild(label);
        list.appendChild(item);

    });

    sourceBox.appendChild(heading);
    sourceBox.appendChild(list);

    return sourceBox;

}

/* ============================================
   Welcome
============================================ */

function removeWelcomeCard() {

    const welcome = document.querySelector(".welcome-card");

    if (welcome) {

        welcome.remove();

    }

}

/* ============================================
   Typing
============================================ */

function showTyping() {

    if (typingIndicator) {

        typingIndicator.classList.remove("hidden");

    }

    scrollBottom();

}

function hideTyping() {

    if (typingIndicator) {

        typingIndicator.classList.add("hidden");

    }

}

/* ============================================
   Scroll
============================================ */

function scrollBottom() {

    requestAnimationFrame(() => {

        chatContainer.scrollTop = chatContainer.scrollHeight;

    });

}

/* ============================================
   Auto Resize
============================================ */

function autoResize() {

    questionInput.style.height = "auto";
    questionInput.style.height = questionInput.scrollHeight + "px";

}

/* ============================================
   Clear Chat
============================================ */

function clearMessages() {

    chatContainer
        .querySelectorAll(".message")
        .forEach(message => message.remove());

}
