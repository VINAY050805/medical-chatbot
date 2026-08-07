/* ============================================
   Medical AI Assistant API Service
============================================ */

const API = {

    BASE_URL: window.MEDICAL_AI_API_BASE_URL || "http://127.0.0.1:8000",

    ENDPOINTS: {

        HEALTH: "/health",

        UPLOAD: "/upload/",

        ASK: "/ask/"

    },

    TIMEOUT: 60000

};

/* ============================================
   Fetch With Timeout
============================================ */

async function fetchWithTimeout(url, options = {}) {

    const controller = new AbortController();

    const timeout = setTimeout(() => {

        controller.abort();

    }, API.TIMEOUT);

    try {

        const response = await fetch(url, {

            ...options,

            signal: controller.signal

        });

        clearTimeout(timeout);

        return response;

    }

    catch (error) {

        clearTimeout(timeout);

        throw error;

    }

}

/* ============================================
   Upload PDFs
============================================ */

async function uploadPDFs(files) {

    const formData = new FormData();

    files.forEach(file => {

        formData.append("files", file);

    });

    try {

        const response = await fetchWithTimeout(

            API.BASE_URL +

            API.ENDPOINTS.UPLOAD,

            {

                method: "POST",

                body: formData

            }

        );

        if (!response.ok) {

            let message = "Upload Failed";

            try {

                const err = await response.json();

                message =

                    err.detail ||

                    err.message ||

                    message;

            }

            catch {}

            throw new Error(message);

        }

        return await response.json();

    }

    catch (error) {

        console.error(

            "Upload Error:",

            error

        );

        throw error;

    }

}

/* ============================================
   Ask Question
============================================ */

async function askQuestion(question) {

    try {

        const response = await fetchWithTimeout(

            API.BASE_URL +

            API.ENDPOINTS.ASK,

            {

                method: "POST",

                headers: {

                    "Content-Type":

                    "application/json"

                },

                body: JSON.stringify({

                    question

                })

            }

        );

        if (!response.ok) {

            let message =

                "Unable to get answer.";

            try {

                const err = await response.json();

                message =

                    err.detail ||

                    err.message ||

                    message;

            }

            catch {}

            throw new Error(message);

        }

        return await response.json();

    }

    catch (error) {

        console.error(

            "Ask Error:",

            error

        );

        throw error;

    }

}

/* ============================================
   Backend Health
============================================ */

async function checkServer() {

    try {

        const response = await fetchWithTimeout(

            API.BASE_URL +

            API.ENDPOINTS.HEALTH

        );

        return response.ok;

    }

    catch {

        return false;

    }

}

/* ============================================
   Get Backend Status
============================================ */

async function backendStatus() {

    const online = await checkServer();

    if (online) {

        console.log(

            "Backend Connected"

        );

    }

    else {

        console.warn(

            "Backend Offline"

        );

    }

    return online;

}
