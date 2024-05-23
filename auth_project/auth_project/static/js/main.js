function keyHandler(key) {
    var btn = 0 || key.keyCode || key.charCode; 
    if (btn == 13) { 
        key.preventDefault(); 
    } 
}

let login = document.getElementById("login"); 
login.onkeydown = keyHandler;

let regis = document.getElementById("sign-up"); 
regis.onkeydown = keyHandler;

var span = document.querySelector("span");

span.addEventListener("input", function() {
	var text = this.innerText;
	this.setAttribute("data-heading", text);
	this.parentElement.setAttribute("data-heading", text);
});