function toggleModes(radioUO, radioEPI, cbLocation, cbExperimentalLocation, cbClassType) {
    var uo = document.getElementById(radioUO);
    var epi = document.getElementById(radioEPI);

    var location = document.getElementById(cbLocation);
    var experimentalLocation = document.getElementById(cbExperimentalLocation);
    var classType = document.getElementById(cbClassType);

    if (uo.checked) {
        location.disabled = true;
        experimentalLocation.disabled = true;
        location.checked = false;
        experimentalLocation.checked = false;
        classType.checked = true;
    } else {
        location.disabled = false;
        experimentalLocation.disabled = false;
        location.checked = true;
        experimentalLocation.checked = true;
        classType.checked = true;
    }
}

function clearCookie(idCookie) {
    document.getElementById(idCookie).value = "";
}

function verifyCookie(idCookie, idSubmit) {
    var cookieDom = document.getElementById(idCookie);
    var submit = document.getElementById(idSubmit);
    var cookie = cookieDom.value;

    console.log(cookie.innerHTML);
    if (cookie.length == 37) {
        if (cookie.charAt(0) == '0' && cookie.charAt(1) == '0' && cookie.charAt(2) == '0' && cookie.charAt(3) == '0'
            && cookie.charAt(27) == ':' && cookie.charAt(28) == '1' && cookie.charAt(29) == 'd') {
            submit.disabled = false;
            cookieDom.classList.add("text-input-correct");
        }
    } else {
        submit.disabled = true;
        cookieDom.classList.remove("text-input-correct");
    }

}
