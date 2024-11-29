const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

$("#uploader").addEventListener("change", function () {
    const image = this.files[0];
    const reader = new FileReader();

    reader.onload = () => {
        const imgUrl = reader.result;
        const img = document.createElement("img");
        img.src = imgUrl
        $("#img-area").appendChild(img);
    }

    reader.readAsDataURL(image);
})
