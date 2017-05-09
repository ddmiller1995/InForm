import React from 'react';
import {store, setCurrentYouth} from "./shared-state.js";
import {Link, IndexLink} from "react-router";
import { formatDate, formatTime, registerDialog, closeDialog, postRequest } from '../util.js'
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
                <td className="exit-column">
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

    render() {
        let exitColumn = this.checkIfPresentationMode();
        let duration = this.checkExitDate();
        let AM = "NA / ", PM = "NA";
        if (this.props.youth.school_am_pickup_time) {
            AM = formatTime(this.props.youth.school_am_pickup_time) + " AM / "
        }
        if (this.props.youth.school_pm_dropoff_time) {
            PM = formatTime(this.props.youth.school_pm_dropoff_time) + " PM"
        }

        return (
            <tr>
                <td className="mdl-data-table__cell--non-numeric">{this.wrapIndexLink(this.props.youth.name)}</td>
                <td>{this.wrapIndexLink(formatDate(this.props.youth.dob))}</td>
                <td>{this.wrapIndexLink(formatDate(this.props.youth.visit_start_date))}</td>
                <td>{this.wrapIndexLink(this.props.youth.current_placement_type.name)}</td>
                <td>{this.wrapIndexLink(this.props.youth.school.school_name || DEFAULT_VALUE)}</td>
                <td>{this.wrapIndexLink(this.props.youth.school_am_transport || DEFAULT_VALUE)}</td>
                <td>{this.wrapIndexLink(this.props.youth.school_pm_transport || DEFAULT_VALUE)}</td>
                <td>{this.wrapIndexLink(AM + PM)}</td>
                <td>{this.wrapIndexLink(this.props.youth.overall_form_progress)}</td>
                <td className={duration}>{this.wrapIndexLink(formatDate(this.props.youth.estimated_exit_date))}</td>
                {exitColumn}
            </tr>
        );
    } 
}