var moment = require("moment");

export function formatDate(date) {
    return moment(date).format('MM/DD/YYYY')
}

export function getDateDiff(start, end) {
    return moment().diff(start, "years") - moment().diff(end, "years");
}