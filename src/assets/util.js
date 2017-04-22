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