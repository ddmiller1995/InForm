var moment = require("moment");

export function formatDate(date) {
    return moment(date).format('MM/DD/YYYY')
}

export function getDateDiff(dob, unit) {
    return moment().diff(dob, unit);
}