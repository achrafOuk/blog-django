text = document.getElementsByClassName("article-content");
for (let i = 0; i < text.length; i++) {
  let inputt = text[i].innerText;
  console.log(":" + inputt);
  if (inputt !== "undefined" || inputt.length > 0) {
    let slideLength = inputt.length > 100 ? 100 : inputt.length;
    text[i].innerText = inputt.slice(0, slideLength) + "...";
  }
}
