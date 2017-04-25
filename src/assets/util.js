var moment = require("moment");

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

export function registerDialog(parentNode, child) {
    let modal = document.getElementById("mdl-dialog");
    if (modal != null) {
        let dialog = document.querySelector("dialog");
        if (!dialog.showModal) {
            dialogPolyfill.registerDialog(dialog);
        }

        dialog.showModal();
        document.getElementById("dialog-close").addEventListener("click", function () {
            dialog.open = "true";
            dialog.close();
            let parent = document.querySelector(parentNode);
            parent.removeChild(parent.childNodes[child]);
        });
    }
}