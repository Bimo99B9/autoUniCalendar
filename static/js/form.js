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