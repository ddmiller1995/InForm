import React from "react";
import {Link, IndexLink} from "react-router";
import { formatDate, getDateDiff } from '../util.js'
import "whatwg-fetch";


const DEFAULT_VALUE = "Not Provided"
let selectedVisit;

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            visitIndex: 0
        };
    }

    getVisits(visits, visitDates) {
        visits.forEach(function(visit) {
            let key = visit.visit_start_date;
            visitDates.push(<option key={key} value={key}>{formatDate(key)}</option>);
        });

        selectedVisit = visitDates[this.state.visitIndex].key;

        return visitDates;
    }

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
                <button className="mdl-button mdl-js-button extend">
                    <i className="material-icons">schedule</i>Extend Stay
                </button>
                {/*<span className="extend-input"><label htmlFor="extend-input">Extend:</label>
                    <input id="extend-input" type="text" autoFocus/>
                </span>*/}

                <button className="mdl-button mdl-js-button change-beds">
                    <i className="material-icons">hotel</i>Change Beds
                </button>
                {/*<span className="bed-input"><label htmlFor="bed-input">Change:</label>
                    <input id="bed-input" type="text" autoFocus/>
                </span>*/}
            </div>
        );
    }
    
    render() {
        let visitDates = [];
        let currentVisit;
        if (this.props.currentYouth.youth_visits) {
            let visits = this.props.currentYouth.youth_visits;
            visitDates = this.getVisits(visits, visitDates);

            currentVisit = visits[this.state.visitIndex];
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
                            <p>Ethnicity: <span className="value"></span></p>
                            <p>City: <span className="value">{currentVisit.city_of_origin || DEFAULT_VALUE}</span></p>
                        </div>
                    </div>
                    <div className="youth-col case">
                        <div className="col-text">
                            <h4>Case</h4>
                            <hr className="youth-info-divider"/>
                        </div>
                        <div className="inner-col">
                            <p>Case Manager: <span className="value">{currentVisit.case_manager.username || DEFAULT_VALUE}</span></p>
                            <p>Personal Counselor: <span className="value">{currentVisit.personal_counselor.username || DEFAULT_VALUE}</span></p>
                            <p>Placement Date: 
                                <span className="value"> {formatDate(currentVisit.current_placement_type.current_placement_start_date)}</span>
                            </p>
                            <p>Placement:  
                                <span className="value"> {currentVisit.current_placement_type.name}
                                    <span className="value"> - { currentVisit.current_placement_type.default_stay_length} days</span>
                                    <span className="value"> - { currentVisit.current_placement_type.current_placement_extension_days} extension days</span>
                                </span>
                            </p>
                            <p>Expected Exit: <span className="value">{formatDate(currentVisit.estimated_exit_date)}</span></p>
                        </div>
                        <div className="inner-col">
                            <p>Referred By: <span className="value">{currentVisit.referred_by || DEFAULT_VALUE}</span></p>
                            <p>Social Worker: <span className="value"></span></p>
                            <p>Bed Nights: <span className="value">{getDateDiff(currentVisit.current_placement_type.current_placement_start_date, "days")}</span></p>
                            <p>Where Exited: <span className="value">{currentVisit.exited_to || DEFAULT_VALUE}</span></p>
                            <p>Permanent Housing: <span className="value">{currentVisit.permanent_housing || DEFAULT_VALUE}</span></p>
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
                        <p>AM Pickup Time: <span className="value"></span></p>
                        <p>AM Phone: <span className="value">{currentVisit.school_am_phone || DEFAULT_VALUE}</span></p>
                    </div>
                    <div className="inner-col">
                        <p>PM Transport: <span className="value">{currentVisit.school_pm_transport || DEFAULT_VALUE}</span></p>
                        <p>PM Dropoff Time: <span className="value">{currentVisit.school_pm_dropoff_time || DEFAULT_VALUE}</span></p>
                        <p>PM Phone: <span className="value">{currentVisit.school_pm_phone || DEFAULT_VALUE}</span></p>
                    </div>
                    <div className="inner-col">
                        <p>Date Requested: <span className="value"></span></p>
                        <p>MKV Complete: <span className="value"></span></p>
                    </div>
                </div>
                <div className="youth-row">
                    <div className="col-text">
                        <h4>Notes</h4>
                        <hr className="youth-info-divider"/>
                    </div>
                </div>
            </div>
        );
    }
}


