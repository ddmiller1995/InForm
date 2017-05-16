var moment = require("moment");
import * as Cookies from "js-cookie";

export function formatDate(date) {
    if (date == null) {
        return;
    }
    return moment(date).format('M/DD/YYYY')
}

export function getDateDiff(dob, unit) {
    if (dob == null) {
        return;
    }
    return moment().diff(dob, unit);
}

export function formatTime(time) {
    if (time == null) {
        return;
    }
    return moment(time, "hh:mm").format("h:mm");
}

export function calcPercentage(number) {
    return Math.round(number * 100) + "%";
}

export function registerDialog(parentNode, child) {

    let modal = document.getElementById("mdl-dialog");
    if (modal != null) {
        let dialog = document.querySelector("dialog");
        if (!dialog.showModal) {
            dialogPolyfill.registerDialog(dialog);
        }

        dialog.showModal();
        document.getElementById("dialog-close").addEventListener("click", function () {
            closeDialog(dialog, parentNode, child);
        });
    }
}

export function closeDialog(dialog, parentNode, child) {
    dialog.open = "true";
    dialog.close();
    let parent = document.querySelector(parentNode);
    parent.removeChild(parent.childNodes[child]);
}

export function getRequest(url, that, prop) {
    let csrf_token = Cookies.get('csrftoken');

    fetch(url, {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": csrf_token,
        }
    }).then(function(response) {
        return response.json();
    }).then(function(data) {
        that.setState({ [prop]: data});
    }).catch(function(ex) {
        console.log("parsing failed", ex);
    });
}

export function postRequest(url, data, reload=true) {
    let csrf_token = Cookies.get('csrftoken');
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": csrf_token,
        },
        body: data
    }).then(function(response) {
        if(reload) {
            window.location.reload();
        }
        return response.json();
    }).then(function(data) {
        console.log(data); // log the response json
    }).catch(function(ex) {
        console.log("parsing failed", ex);
    });
}
export function titleCase(s) {
    let words = s.split(' ');
    for(let i = 0; i < words.length; i++) {
        words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1);
    }
    return words.join(' ');
}