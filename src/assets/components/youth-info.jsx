import React from "react";
import ReactDOM from "react-dom";
import {Link, IndexLink} from "react-router";
import { formatDate, getDateDiff, formatTime, registerDialog, 
    closeDialog, postRequest, getRequest } from '../util.js'
import "whatwg-fetch";

var moment = require("moment");

const PLACEMENT_API = "/api/placement-type";
const DEFAULT_VALUE = "Not Provided"
let selectedVisit;

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            visitIndex: 0,
        };
    }

    componentDidMount() {
        let data = getRequest(PLACEMENT_API, this, "placement_types");
    }

    // populate the visit date dropdown with all the visits of this particular youth
    getVisits(visits, visitDates) {
        visits.forEach(function(visit) {
            let key = visit.visit_start_date;
            visitDates.push(<option key={key} value={key}>{formatDate(key)}</option>);
        });

        selectedVisit = visitDates[this.state.visitIndex].key;
        return visitDates;
    }

    // grab the visit date currently selected in the visit dropdown
    getSelectedVisit(evt) {
        let that = this;
        let dropdown = document.querySelector(".mdl-select__input");
        if (dropdown != null) {
            selectedVisit = evt.target.options[evt.target.selectedIndex].value;

            let visits = this.props.currentYouth.youth_visits;
            visits.forEach(function(visit, index) {
                let key = visit.visit_start_date;
                if (key === selectedVisit) {
                    that.setState({
                        visitIndex: index
                    });
                }
            });
        }
    }

    renderActionButtons() {
        return (
            <div className="youth-action-buttons">
                <button className="mdl-button mdl-js-button extend" onClick={() => this.toggleModal("extend")}>
                    <i className="material-icons">schedule</i>Extend Stay
                </button>

                <button className="mdl-button mdl-js-button change-beds" onClick={() => this.toggleModal("switch")}>
                    <i className="material-icons">hotel</i>Change Beds
                </button>
                <button className="mdl-button mdl-js-button edit-youth">
                    <a className="mdl-navigation__link" href={"/admin/api/youthvisit/" + 
                        this.props.currentYouth.youth_visits[this.state.visitIndex].youth_visit_id + "/change/"}>
                        <i className="material-icons">mode_edit</i>
                        Edit Visit Details
                    </a>
                </button>
            </div>
        );
    }

    toggleModal(action) {
        let that = this;
        let postFunction;
        let div;
        if (action === "extend") {
            div = this.buildExtendModal();
            postFunction = this.postExtend;
        } else {
            div = this.buildSwitchModal();
            postFunction = this.postSwitch;
        }
        // if dialog doesn't exist, append it
        if (document.getElementById("mdl-dialog") == null) {
            document.querySelector(".youth-info-container").appendChild(div.firstElementChild);
        } 

        this.changeEstimatedDate();
        this.setPlacementTypes();
        // @param1: parent container that dialog child will be added and removed from
        // @param2: index of dialog in childNodes array
        registerDialog(".youth-info-container", 5);
        // create post request on "save", then close modal
        document.getElementById("submit-dialog").addEventListener("click", function () {
            postFunction(that);
            let dialog = document.querySelector("dialog");
            closeDialog(dialog, ".youth-info-container", 5);
        });
    }

    buildExtendModal() {
        let div = document.createElement("div");
        let modal = (`
            <dialog id="mdl-dialog">
                <h4 id="dialog-title">Extend Stay</h4>
                <div id="dialog-descr">
                    <p>Extend stay for ${this.props.currentYouth.name}</p>
                    <p>Current extension days: 
                        ${this.props.currentYouth.youth_visits[this.state.visitIndex].current_placement_type.current_placement_extension_days}
                    </p>
                    <p>Extend by 
                        <span>
                            <input id="extend-input" type="number" value="15"></input>
                        </span> days
                    </p>
                    <p>New estimated exit: <span id="new-estimate"></span></p>
                </div>
                <div id="dialog-actions">
                    <button class="mdl-button mdl-js-button" type="button" id="submit-dialog">Save</button>
                    <button class="mdl-button mdl-js-button" type="button" id="close-dialog">Cancel</button>
                </div>
            </dialog>
        `);

        div.innerHTML = modal;
        return div;
    }
    
    buildSwitchModal() {
        let div = document.createElement("div");
        let today = moment().format("YYYY-MM-DD");
        let modal = (`
            <dialog id="mdl-dialog">
                <h4 id="dialog-title">Switch Beds</h4>
                <div id="dialog-descr">
                    <p>Switch beds for ${this.props.currentYouth.name}</p>
                    <p>Current placement: 
                        ${this.props.currentYouth.youth_visits[this.state.visitIndex].current_placement_type.name}
                    </p>
                    <p>New placement: 
                        <span><select className="mdl-select__input" id="placement-dropdown" name="placement"></select></span>
                    </p>
                    <p>Transfer Date: <span><input id="date-input" type="date" value=`+today+`></input></span></p>
                </div>
                <div id="dialog-actions">
                    <button type="button" class="mdl-button mdl-js-button" id="submit-dialog">Save</button>
                    <button type="button" class="mdl-button mdl-js-button" id="close-dialog">Cancel</button>
                </div>
            </dialog>
        `);

        div.innerHTML = modal;
        return div;
    }

    // on the extend modal, update the estimated exit date according to the user-inputted
    // extend days
    changeEstimatedDate() {
        let exit = this.props.currentYouth.youth_visits[this.state.visitIndex].estimated_exit_date;
        let extend = document.getElementById("extend-input");
        if (extend != null) {
            let update = function updateEstimate() {
                let date = new Date(exit);
                date.setTime( date.getTime() + date.getTimezoneOffset()*60*1000);
                date.setDate(date.getDate() + parseInt(extend.value));

                let day = date.getDate();
                let month = date.getMonth() + 1;
                let year = date.getFullYear();

                let newExit = document.getElementById("new-estimate");
                newExit.textContent = month + "/" + day + "/" + year;

            };
            update();
            extend.addEventListener("input", update);
        }
    }

    // on the switch modal, populate the dropdown with all the placement types
    setPlacementTypes() {
        let change = document.getElementById("placement-dropdown");
        if (change != null) {
            this.state.placement_types.forEach(function(type) {
                let option = document.createElement("option");
                option.textContent = type.placement_type_name;
                option.value = type.id;
                change.appendChild(option);
            });
        }
    }

    postExtend(that) {
        let visitID = that.props.currentYouth.youth_visits[that.state.visitIndex].youth_visit_id;
        let url = "/api/visit/" + visitID + "/add-extension/";
        let extension = document.getElementById("extend-input").value;
        let data = new FormData();
        data.append("extension", extension);

        postRequest(url, data);
    }

    postSwitch(that) {
        let visitID = that.props.currentYouth.youth_visits[that.state.visitIndex].youth_visit_id;
        let url = "/api/visit/" + visitID + "/change-placement/";
        let placementID = document.getElementById("placement-dropdown").value;
        let placementStartDate = document.getElementById("date-input").value;
        let data = new FormData();
        data.append("new_placement_type_id", placementID);
        data.append("new_placement_start_date", placementStartDate);

        postRequest(url, data);
    }

    postNotes() {
        let visitID = this.props.currentYouth.youth_visits[this.state.visitIndex].youth_visit_id;
        let url = "/api/visit/" + visitID + "/edit-note/";
        let notes = document.getElementById("notes-input").value;
        let data = new FormData();
        data.append("note", notes);

        postRequest(url, data);
    }

    setYesOrNo(currentVisit, data) {
        if (currentVisit[data]) {
            return "Yes";
        } else if (currentVisit[data] === false) {
            return "No"; 
        }
    }

    render() {
        let visitDates = [];
        let currentVisit, currentPlacement;
        let AM, PM, permHousing, mkv, guardian, relationship;
        if (this.props.currentYouth.youth_visits) {
            let visits = this.props.currentYouth.youth_visits;
            visitDates = this.getVisits(visits, visitDates);

            currentVisit = visits[this.state.visitIndex];

            if (currentVisit.school_am_pickup_time) {
                AM = formatTime(currentVisit.school_am_pickup_time) + " AM"
            }
            if (currentVisit.school_pm_dropoff_time) {
                PM = formatTime(currentVisit.school_pm_dropoff_time) + " PM"
            }

            permHousing = this.setYesOrNo(currentVisit, "permanent_housing"); 
            mkv = this.setYesOrNo(currentVisit, "school_mkv_complete");

            if (currentVisit.guardian_name) {
                guardian = currentVisit.guardian_name;
                if (currentVisit.guardian_relationship) {
                    relationship = " (" + currentVisit.guardian_relationship + ")";
                } else {
                    relationship = "";
                }
            }
        }

        if (currentVisit == null) {
            return null;
        }

        return (
            <div className="container youth-info-container">
                <div className="mdl-select mdl-js-select mdl-select--floating-label">
                    <label className="mdl-select__label" htmlFor="visit">Visit Date </label>
                    <select className="mdl-select__input" id="visit" name="visit" onChange={(evt) => this.getSelectedVisit(evt)}>
                        {visitDates}
                    </select>
                </div>

                {this.renderActionButtons()}

                <div className="youth-row">
                    <div className="youth-col personal">
                        <div className="col-text">
                            <h4>Personal</h4>
                            <hr className="youth-info-divider"/>
                            <p>Name: <span className="value">{this.props.currentYouth.name}</span></p>
                            <p>Birthdate: <span className="value">{formatDate(this.props.currentYouth.dob)}</span></p>
                            <p>Age: <span className="value">{getDateDiff(this.props.currentYouth.dob, "years")}</span></p>
                            <p>Guardian: <span className="value">{guardian + relationship || DEFAULT_VALUE}</span></p>
                            <p>City: <span className="value">{currentVisit.city_of_origin || DEFAULT_VALUE}</span></p>
                        </div>
                    </div>
                    <div className="youth-col case">
                        <div className="col-text">
                            <h4>Case</h4>
                            <hr className="youth-info-divider"/>
                        </div>
                        <div className="inner-col">
                            <p>Entry Date: <span className="value">{formatDate(currentVisit.visit_start_date)}</span></p>
                            <p>Bed Nights: 
                                <span className="value">{currentVisit.total_bed_nights}</span>
                            </p>
                            <p>Current Placement Date:  
                                <span className="value"> 
                                    {formatDate(currentVisit.current_placement_type.current_placement_start_date)}
                                </span>
                            </p>
                            <p>Placement Type:  
                                <span className="value"> {currentVisit.current_placement_type.name}</span>
                            </p>
                            <p>Estimated Stay:  
                                <span className="value"> { currentVisit.current_placement_type.default_stay_length} days (+ 
                                    { currentVisit.current_placement_type.current_placement_extension_days} day extension)
                                </span>
                            </p>
                        </div>
                        <div className="inner-col">
                            <p>Case Manager: <span className="value">{currentVisit.case_manager.full_name || currentVisit.case_manager.username || DEFAULT_VALUE}</span></p>
                            <p>Personal Counselor: <span className="value">{currentVisit.personal_counselor.full_name || currentVisit.personal_counselor.username || DEFAULT_VALUE}</span></p>
                            <p>Social Worker: <span className="value">{currentVisit.social_worker || DEFAULT_VALUE}</span></p>
                            <p>Referred By: <span className="value">{currentVisit.referred_by || DEFAULT_VALUE}</span></p>
                        </div>
                        <div className="inner-col">
                            <p>Estimated Exit: <span className="value">{formatDate(currentVisit.estimated_exit_date)}</span></p>
                            <p>Actual Exit: <span className="value">{formatDate(currentVisit.visit_exit_date) || "N/A"}</span></p>
                            <p>Where Exited: <span className="value">{currentVisit.exited_to || DEFAULT_VALUE}</span></p>
                            <p>Permanent Housing: <span className="value">{permHousing || DEFAULT_VALUE}</span></p>
                        </div>
                    </div>
                </div>
                <div className="youth-row">
                    <div className="col-text">
                        <h4>School</h4>
                        <hr className="youth-info-divider"/>
                    </div>
                    <div className="inner-col">
                        <p>School: <span className="value">{currentVisit.school.school_name || DEFAULT_VALUE}</span></p>
                        <p>District: <span className="value">{currentVisit.school.school_district || DEFAULT_VALUE}</span></p>
                        <p>Phone: <span className="value">{currentVisit.school.school_phone || DEFAULT_VALUE}</span></p>
                    </div>
                    <div className="inner-col">
                        <p>AM Transport: <span className="value">{currentVisit.school_am_transport || DEFAULT_VALUE}</span></p>
                        <p>AM Pickup Time: <span className="value">{AM || DEFAULT_VALUE}</span></p>
                        <p>AM Phone: <span className="value">{currentVisit.school_am_phone || DEFAULT_VALUE}</span></p>
                    </div>
                    <div className="inner-col">
                        <p>PM Transport: <span className="value">{currentVisit.school_pm_transport || DEFAULT_VALUE}</span></p>
                        <p>PM Dropoff Time: <span className="value">{PM || DEFAULT_VALUE}</span></p>
                        <p>PM Phone: <span className="value">{currentVisit.school_pm_phone || DEFAULT_VALUE}</span></p>
                    </div>
                    <div className="inner-col">
                        <p>Date Requested: 
                                <span className="value">{formatDate(currentVisit.school_date_requested) || DEFAULT_VALUE}</span></p>
                        <p>MKV/Enroll Complete: <span className="value">{mkv || DEFAULT_VALUE}</span></p>
                    </div>
                </div>
                <div className="youth-row">
                    <div className="col-text">
                        <h4>Visit Notes</h4>
                        <hr className="youth-info-divider"/>
                        <textarea name="notes" id="notes-input" cols="30" rows="10" defaultValue={currentVisit.visit_notes}></textarea>
                        <button 
                            className="mdl-button mdl-js-button save-notes" 
                            onClick={() => this.postNotes()}>Save
                        </button>
                    </div>
                </div>
            </div>
        );
    }
}


