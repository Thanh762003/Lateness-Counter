const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

function toggleStream() {
	fetch("/toggle-stream", { method: "POST" }).catch((err) => console.log(err));
}

window.addEventListener("load", () => {
    $("#stream-btn").addEventListener("click", toggleStream);
})
