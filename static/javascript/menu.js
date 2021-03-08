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
    display("navbar-collapse collapse", 1);
  });
function displayMenu() {
  let toggle = document.getElementsByClassName("dropdown-menu")[0].style
    .display;
  document.getElementsByClassName("dropdown-menu")[0].style.display =
    document.getElementsByClassName("dropdown-menu")[0].style.display ===
    "block"
      ? "none"
      : "block";
}
document
  .getElementsByClassName("dropdown-toggle")[0]
  .addEventListener("click", function () {
    displayMenu();
  });
