import React from 'react';
import {store, setCurrentYouth} from "./shared-state.js";
import {Link, IndexLink} from "react-router";
import { formatDate, formatTime, registerDialog} from '../util.js'
import { closeDialog, postRequest, calcPercentage } from '../util.js'
import "whatwg-fetch";

var moment = require("moment");
const DEFAULT_VALUE = "Not Provided"

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = store.getState();
    }

    componentDidMount() {
        this.unsub = store.subscribe(() => this.setState(store.getState()));
    }

    componentWillUnmount() {
        this.unsub();
    }

    wrapIndexLink(data) {
        return (
            <IndexLink 
                className="mdl-navigation__link" 
                to="/youth"
                key={data} 
                onClick={() => this.registerYouth()}>
                {data}
            </IndexLink>
        );
    }

    registerYouth() {
        store.dispatch(setCurrentYouth(this.props.youth));
        window.location.reload();
    }

    postExit() {
        let url = "/api/visit/" + this.props.youth.youth_visit_id + "/mark-exited/";
        let exitDate = document.getElementById("date-input").value;
        let whereExited = document.getElementById("exited-to-input").value;
        let permHousing = $('input[name="housing"]:checked').val();
        let data = new FormData();
        data.append("exit_date_string", exitDate);
        data.append("where_exited", whereExited);
        data.append("permanent_housing", permHousing);

        postRequest(url, data);
    }

    toggleModal() {
        let that = this;
        let div = this.buildDialog();
        // if dialog doesn't exist, append it
        if (document.getElementById("mdl-dialog") == null) {
            document.querySelector(".youth-tracker-container").appendChild(div.firstElementChild);
        } 
        // @param1: parent container that dialog child will be added and removed from
        // @param2: index of dialog in childNodes array
        registerDialog(".youth-tracker-container", 2);
        // create post request on "save", then close modal
        document.getElementById("dialog-submit").addEventListener("click", function () {
            that.postExit();
            let dialog = document.querySelector("dialog");
            closeDialog(dialog, ".youth-tracker-container", 2);
        });
    }

    buildDialog() {
        let div = document.createElement("div"); 
        let today = moment().format("YYYY-MM-DD");
        let modal = (`
            <dialog id="mdl-dialog" className="exit-dialog">
                <h4 id="dialog-title">Mark ${this.props.youth.name} exited</h4>
                <div id="exit-warning">
                    <p>
                        <i>Only mark a youth as exited if they have left the shelter. For extending stays 
                        or changing beds, please go <a href="#youth">here</a></i>
                    </p>
                </div>
                <div id="dialog-descr">
                    <p>Exit Date: <span><input id="date-input" type="date" value=`+today+`></input></span></p>
                    <p>Where did they exit to? <span><input id="exited-to-input" type="text"></input></span></p>
                    <p>Permanent Housing? 
                        <span> 
                         <input id="yes-checkbox" name="housing" type="radio" value="true"></input>Yes 
                         <input id="no-checkbox" name="housing" type="radio" value="false"></input>No 
                         <input id="unknown-checkbox" name="housing" type="radio" value="unknown"></input>Unknown 
                        </span>
                    </p>
                </div>
                <div id="dialog-actions">
                    <button type="button" id="dialog-submit">Save</button>
                    <button type="button" id="dialog-close">Cancel</button>
                </div>
            </dialog>
        `);

        div.innerHTML = modal;
        return div;
    }

    checkIfPresentationMode() {
        let parent = document.querySelector("thead").parentNode.className;
        if (parent.includes("presentation")) {
            return
        } else {
            return (
                <td key={this.props.youth.visit_exit_date} className="exit-column">
                    {formatDate(this.props.youth.visit_exit_date) ||
                    <button className="mdl-button mdl-js-button add-exit" onClick={() => this.toggleModal()}>
                        <i className="material-icons add-exit-icon">add</i>Add
                    </button>}
                </td>
            );
        }
    }

    checkExitDate() {
        let from = moment(moment(), "YYYY-MM-DD"); 
        let to = moment(this.props.youth.estimated_exit_date, "YYYY-MM-DD");
        let duration = to.diff(from, 'days')

        if (duration <= 3) {
            return "three-days";
        } else if (duration <= 7) {
            return "seven-days";
        } else {
            return ""
        }
    }

    // Create the HTML cells for each field
    getCells() {
        let cells = [];
        let duration = this.checkExitDate();
        if(this.props.fields) {
            for(let i = 0; i < this.props.fields.length; i++) {
                let field = this.props.fields[i];
                // Special case that needs a CSS class added
                if(field.field_path == "estimated_exit_date") {
                    cells.push(<td key={field.field_name} className={duration}>{this.wrapIndexLink(this.parseFieldPath(field.field_path))}</td>);
                } else {
                    cells.push(<td key={field.field_name} >{this.wrapIndexLink(this.parseFieldPath(field.field_path))}</td>);
                }
            }
            // Add the "+ Add" Exit Date button in not in presentation mode
            cells.push(this.checkIfPresentationMode()); 
        }
        return cells;
    }

    // Using the formating field path value, lookup and format the string value to display
    parseFieldPath(path) {
        let parts = path.split('|');
        let value = this.props.youth;

        // Special case for combining both AM and PM time values into one column
        if(path == "am+pm") {
            let AM = "NA / ", PM = "NA";
            if (value.school_am_pickup_time) {
                AM = formatTime(value.school_am_pickup_time) + " AM / "
            }
            if (value.school_pm_dropoff_time) {
                PM = formatTime(value.school_pm_dropoff_time) + " PM"
            }
            return AM + PM;
        }

        // Special case for formatting the percentage
        if(path == "overall_form_progress") {
            return calcPercentage(value[path]);
        }

        // Iteratively lookup the value  in the object
        for(let i = 0; i < parts.length; i++) {
            let part = parts[i].trim();
            value = value[part];
        }

        // Regex for the expected date format
        let pattern = /\d{4}-\d{2}-\d{2}/;

        if(value == null || value == '') {
            value = DEFAULT_VALUE;
        // Format the date to a more readable format if the value is a date
        } else if(value.match(pattern) != null) {
            value = formatDate(value);
        }
        return value
    }

    render() {
        let cells = this.getCells();

        return (
            <tr>
                {cells}
            </tr>
        )
    } 
}