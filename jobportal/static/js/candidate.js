
function openModal(email) {
    document.getElementById("messageModal").classList.remove("hidden");
    document.getElementById("messageModal").classList.add("flex");

    document.getElementById("candidateEmail").value = email;
}

function closeModal() {
    document.getElementById("messageModal").classList.remove("flex");
    document.getElementById("messageModal").classList.add("hidden");
}
