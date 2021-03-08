text = document.getElementsByClassName("card-text");
for (let i = 0; i < text.length; i++) {
  let inputt = text[i].innerText;
  if (inputt !== "undefined" || inputt.length > 0) {
    if (inputt.length > 100) {
      text[i].innerText = inputt.slice(0, 100) + "...";
    }
  }
}
