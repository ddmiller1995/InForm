var moment = require("moment");

export function formatDate(date) {
    return moment(date).format('M/DD/YYYY')
}

export function getDateDiff(dob, unit) {
    return moment().diff(dob, unit);
}

export function formatTime(time) {
    return moment(time, "hh:mm").format("h:mm");
}