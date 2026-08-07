/* ============================================
   Upload Component
============================================ */

let pdfInput;
let uploadBox;
let fileList;

/* ============================================
   Initialize
============================================ */

document.addEventListener("DOMContentLoaded", () => {

    pdfInput = document.getElementById("pdfInput");
    uploadBox = document.querySelector(".upload-box");
    fileList = document.getElementById("fileList");

    if (!pdfInput || !uploadBox || !fileList) {

        console.error("Upload elements not found.");

        return;

    }

    /* Browse */

    pdfInput.addEventListener("change", () => {

        if (pdfInput.files.length > 0) {

            handleUpload([...pdfInput.files]);

        }

    });

    /* Drag */

    uploadBox.addEventListener("dragover", dragOver);

    uploadBox.addEventListener("dragleave", dragLeave);

    uploadBox.addEventListener("drop", dropFiles);

});

/* ============================================
   Drag
============================================ */

function dragOver(e) {

    e.preventDefault();

    uploadBox.classList.add("dragging");

}

function dragLeave() {

    uploadBox.classList.remove("dragging");

}

function dropFiles(e) {

    e.preventDefault();

    uploadBox.classList.remove("dragging");

    const files = [...e.dataTransfer.files];

    handleUpload(files);

}

/* ============================================
   Upload
============================================ */

async function handleUpload(files) {

    const pdfs = [];

    files.forEach(file => {

        if (

            file.type === "application/pdf"

        ) {

            pdfs.push(file);

        }

    });

    if (pdfs.length === 0) {

        showToast(

            "Only PDF files allowed"

        );

        return;

    }

    try {

        uploadBox.classList.add("uploading");

        showToast("Uploading PDFs...");

        const result = await uploadPDFs(pdfs);

        uploadBox.classList.remove("uploading");

        renderFiles(pdfs);

        showToast(

            result.message ||

            "Upload Successful"

        );

        pdfInput.value = "";

    }

    catch (error) {

        uploadBox.classList.remove("uploading");

        console.error(error);

        showToast(

            error.message ||

            "Upload Failed"

        );

    }

}

/* ============================================
   Render Files
============================================ */

function renderFiles(files) {

    files.forEach(file => {

        const id =

            file.name.replace(/\W/g, "_");

        if (

            document.getElementById(id)

        ) return;

        const li =

            document.createElement("li");

        li.id = id;

        const pdfIcon = document.createElement("i");
        pdfIcon.className = "fa-solid fa-file-pdf";

        const info = document.createElement("div");
        info.className = "file-info";

        const name = document.createElement("span");
        name.className = "file-name";
        name.textContent = file.name;

        const size = document.createElement("span");
        size.className = "file-size";
        size.textContent = formatSize(file.size);

        const success = document.createElement("i");
        success.className = "fa-solid fa-circle-check success";

        info.appendChild(name);
        info.appendChild(size);

        li.appendChild(pdfIcon);
        li.appendChild(info);
        li.appendChild(success);

        fileList.appendChild(li);

    });

}

/* ============================================
   File Size
============================================ */

function formatSize(bytes) {

    if (bytes < 1024)

        return bytes + " B";

    if (bytes < 1024 * 1024)

        return (

            (bytes / 1024)

            .toFixed(1)

            + " KB"

        );

    return (

        (bytes / (1024 * 1024))

        .toFixed(1)

        + " MB"

    );

}

/* ============================================
   Toast
============================================ */

function showToast(message) {

    const toast =

        document.getElementById("toast");

    if (!toast) return;

    toast.textContent = message;

    toast.classList.add("show");

    clearTimeout(window.toastTimer);

    window.toastTimer =

        setTimeout(() => {

            toast.classList.remove("show");

        }, 2500);

}

/* ============================================
   Clear Upload List
============================================ */

function clearUploads() {

    fileList.innerHTML = "";

}
