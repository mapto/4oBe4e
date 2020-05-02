function rollDice() {
    var randomNumber = Math.floor(Math.random() * 6) + 1; // 1 - 6
    var playerOneImages = "images/red" +randomNumber+ ".png";

    document.querySelector('.img1').setAttribute('src', playerOneImages)
}

function myFunction1() {
    var x = document.getElementById("player1").value;
    document.getElementById("demo1").innerHTML = x;
  }
function myFunction2() {
    var x = document.getElementById("player2").value;
    document.getElementById("demo2").innerHTML = x;
  }
function myFunction3() {
    var x = document.getElementById("player3").value;
    document.getElementById("demo3").innerHTML = x;
  }
  function myFunction4() {
    var x = document.getElementById("player4").value;
    document.getElementById("demo4").innerHTML = x;
  }