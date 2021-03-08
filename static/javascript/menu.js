function display() {
  let toggle = document.getElementsByClassName("navbar-collapse collapse")[1]
    .style.display;
  document.getElementsByClassName("navbar-collapse")[1].style.display =
    document.getElementsByClassName("navbar-collapse")[1].style.display ===
    "block"
      ? "none"
      : "block";
}
document
  .getElementsByClassName("navbar-toggler")[1]
  .addEventListener("click", function () {
    display();
  });
