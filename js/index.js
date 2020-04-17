var randomNumber = Math.floor(Math.random() * 6) + 1; // 1 - 6
var playerOneImages = "images/red" +randomNumber+ ".png";

document.querySelector('.img1').setAttribute('src', playerOneImages)