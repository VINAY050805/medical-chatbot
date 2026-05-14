const API_BASE = "http://localhost:8000";

async function askQuestion(question) {

    const response = await fetch(`${API_BASE}/ask`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
    });

    const data = await response.json();

    return data.answer;
}