var moment = require("moment");

export function formatDate(date) {
    return moment(date).format('MM/DD/YYYY')
}

export function getDateDiff(dob) {
    return moment().diff(dob, "years");
}