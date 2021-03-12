text = document.getElementsByClassName("card-text");
for (let i = 0; i < text.length; i++) {
  let poster = text[i].querySelector("img");
  let post = text[i].innerText;
  text[i].innerHTML = "";
  if (poster !== "undefined") {
    text[i].append(poster);
  }
  if (post !== "undefined" || post.length > 0) {
    if (post.length > 100) {
      post = post.slice(0, 100) + "...";
    }
    text[i].append(post);
  }
}
