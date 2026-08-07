/* =====================================================
   Medical AI Assistant
===================================================== */

let sidebar;
let overlay;
let menuBtn;
let themeBtn;

/* =====================================================
   Initialize
===================================================== */

document.addEventListener("DOMContentLoaded", async () => {

    sidebar = document.getElementById("sidebar");
    overlay = document.getElementById("overlay");
    menuBtn = document.getElementById("menuBtn");
    themeBtn = document.getElementById("themeToggle");

    initializeTheme();
    initializeSidebar();
    initializeChatControls();

    await initializeBackend();

});

/* =====================================================
   Backend
===================================================== */

async function initializeBackend() {

    const online = await checkServer();

    showToast(
        online
            ? "Backend Connected"
            : "Backend Offline"
    );

}

/* =====================================================
   Theme
===================================================== */

function initializeTheme() {

    const savedTheme = localStorage.getItem("theme") || "light";

    if (savedTheme === "dark") {

        document.body.classList.add("dark");

    }

    updateThemeIcon(document.body.classList.contains("dark"));

    if (themeBtn) {

        themeBtn.addEventListener("click", toggleTheme);

    }

}

function toggleTheme() {

    document.body.classList.toggle("dark");

    const dark = document.body.classList.contains("dark");

    localStorage.setItem("theme", dark ? "dark" : "light");

    updateThemeIcon(dark);

}

function updateThemeIcon(dark) {

    if (!themeBtn) return;

    themeBtn.innerHTML = dark
        ? `<i class="fa-solid fa-sun"></i>`
        : `<i class="fa-solid fa-moon"></i>`;

}

/* =====================================================
   Sidebar
===================================================== */

function initializeSidebar() {

    if (menuBtn) {

        menuBtn.addEventListener("click", openSidebar);

    }

    if (overlay) {

        overlay.addEventListener("click", closeSidebar);

    }

}

function openSidebar() {

    sidebar?.classList.add("active");
    overlay?.classList.add("active");

}

function closeSidebar() {

    sidebar?.classList.remove("active");
    overlay?.classList.remove("active");

}

/* =====================================================
   Chat Buttons
===================================================== */

function initializeChatControls() {

    const newChatBtn = document.querySelector(".new-chat-btn");
    const clearBtn = document.querySelector(".clear-chat");

    if (newChatBtn) {

        newChatBtn.addEventListener("click", startNewChat);

    }

    if (clearBtn) {

        clearBtn.addEventListener("click", clearConversation);

    }

}

/* =====================================================
   New Chat
===================================================== */

function startNewChat() {

    if (!confirm("Start a new conversation?")) return;

    resetChatView();
    resetQuestionInput(true);
    closeSidebar();
    showToast("New Chat Started");

}

function clearConversation() {

    if (!confirm("Clear the current conversation?")) return;

    resetChatView();
    resetQuestionInput(false);
    closeSidebar();
    showToast("Chat Cleared");

}

function resetChatView() {

    const container = document.getElementById("chatContainer");

    if (!container) return;

    container
        .querySelectorAll(".message, .welcome-card")
        .forEach(element => element.remove());

    const welcome = document.createElement("div");
    welcome.className = "welcome-card";
    welcome.innerHTML = `
        <img src="assets/medicalAssistant.png" alt="Medical AI">
        <h2>Welcome</h2>
        <p>Upload one or more medical PDFs and start asking questions.</p>
    `;

    const indicator = document.getElementById("typingIndicator");

    if (indicator) {

        indicator.classList.add("hidden");
        container.insertBefore(welcome, indicator);

    }

    else {

        container.appendChild(welcome);

    }

}

function resetQuestionInput(focus) {

    const input = document.getElementById("questionInput");

    if (!input) return;

    input.value = "";
    input.style.height = "auto";

    if (focus) {

        input.focus();

    }

}

/* =====================================================
   Window Resize
===================================================== */

window.addEventListener("resize", () => {

    if (window.innerWidth > 992) {

        closeSidebar();

    }

});

/* =====================================================
   ESC
===================================================== */

document.addEventListener("keydown", (e) => {

    if (e.key === "Escape") {

        closeSidebar();

    }

});

/* =====================================================
   Prevent Browser Drop
===================================================== */

document.addEventListener("dragover", (e) => {

    e.preventDefault();

});

document.addEventListener("drop", (e) => {

    e.preventDefault();

});
