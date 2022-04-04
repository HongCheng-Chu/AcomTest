
function change_sign(x) {
    x.classList.toggle("change");
    var x = document.getElementById("myLinks");
    if (x.style.display === "block") {
        x.style.display = "none";
    } else {
        x.style.display = "block";
    }
}


function SearchGirls() {
    // Declare variables
    var input, filter, div, btn, i, txtValue;
    input = document.getElementById("q");
    filter = input.value.toUpperCase();
    div = document.getElementById("search-list");
    btn = div.getElementsByTagName("button");

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < btn.length; i++) {
        txtValue = btn[i].textContent || btn[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            btn[i].style.display = "";
        } else {
            btn[i].style.display = "none";
        }
    }
}


function pushcard(evt, name) {
    var i, btn, girl;

    girl = document.getElementsByClassName('dns-content');
    for (i = 0; i < girl.length; i++) {
        girl[i].style.display = "none";
    }

    btn = document.getElementsByClassName("girlname");
    for (i = 0; i < btn.length; i++) {
        btn[i].className = btn[i].className.replace(" active", "");
    }

    document.getElementById(name).style.display = "block";
    evt.currentTarget.className += " active";

    window.scrollTo({top: 0, left: 0 })
}
