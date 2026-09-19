let burger = document.getElementById("burger");
let dropUl = document.getElementById("dropUl");
burger.addEventListener("click", function () {
  dropUl.classList.toggle("active");
});

let selectedRadio = null;
let radios = document.querySelectorAll('input[type="radio"]');

radios.forEach(function (radio) {
  radio.addEventListener("click", function () {
    if (selectedRadio === radio) {
      radio.checked = false;
      selectedRadio = null;
    } else {
      selectedRadio = radio;
    }
  });
});

let phone = document.getElementById("phone");
let submit = document.querySelector(input[(type = "submit")]);
let form = document.getElementById("form");

form.addEventListener("submit", function (e) {
  if (phone.value.type !== number) {
    e.preventDefault;
  }
});
