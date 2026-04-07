// ===== SIDEBAR TOGGLE =====
function toggleSidebar() {
    console.log("Clicked");

    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("main");

    if (!sidebar || !main) {
        alert("Sidebar/Main not found ❌");
        return;
    }

    sidebar.classList.toggle("collapsed");
    main.classList.toggle("collapsed");
};


// ===== ENCRYPT / DECRYPT =====
function action(type, file) {
    const keyInput = document.getElementById("key");

    if (!keyInput) {
        alert("Key input not found!");
        return;
    }

    const key = keyInput.value.trim();

    if (key.length !== 1) {
        alert("⚠️ Enter exactly 1 character key!");
        keyInput.focus();
        return;
    }

    window.location.href = `/${type}/${file}?key=${key}`;
}


// ===== DELETE FILE =====
function deleteFile(file) {
    const confirmDelete = confirm(`Delete file: ${file}?`);

    if (confirmDelete) {
        window.location.href = `/delete/${file}`;
    }
}


// ===== OPTIONAL: ENTER KEY HELP =====
document.addEventListener("DOMContentLoaded", () => {
    const keyInput = document.getElementById("key");

    if (keyInput) {
        keyInput.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                alert("Click Encrypt or Decrypt button after entering key");
            }
        });
    }
});