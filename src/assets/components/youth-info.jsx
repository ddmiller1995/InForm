import React from "react";
import {Link, IndexLink} from "react-router";
import { formatDate, getDateDiff } from '../util.js'
import "whatwg-fetch";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    // showInput() {
        
    // }

    render() {
        return (
            <div className="container youth-info-container">
                <div className="mdl-select mdl-js-select mdl-select--floating-label">
                    <label className="mdl-select__label" htmlFor="visit">Visit Date </label>
                    <select className="mdl-select__input" id="visit" name="visit">
                        <option value=""></option>
                        <option value="option1">Recent</option>
                        <option value="option2">10/13/2015</option>
                        <option value="option3">3/20/2014</option>
                    </select>
                </div>

                <button className="mdl-button mdl-js-button mdl-button--raised extend">Extend Stay</button>
                <span className="extend-input"><label htmlFor="extend-input">Extend:</label>
                    <input id="extend-input" type="text" autoFocus/>
                </span>

                <button className="mdl-button mdl-js-button mdl-button--raised change-beds">Change Beds</button>
                <span className="bed-input"><label htmlFor="bed-input">Change:</label>
                    <input id="bed-input" type="text" autoFocus/>
                </span>

                <div className="youth-row">
                    <div className="youth-col">
                        <div className="col-text">
                            <h4>Personal</h4>
                            <hr className="youth-info-divider"/>
                            <p>Name: {this.props.currentYouth.name}</p>
                            <p>Birthdate: <span>{formatDate(this.props.currentYouth.dob)}</span></p>
                            <p>Age: <span>{getDateDiff(this.props.currentYouth.dob)}</span></p>
                            <p>Ethnicity: <span>{this.props.currentYouth.ethnicity}</span></p>
                            <p>City: <span>{this.props.currentYouth.city_of_origin}</span></p>
                        </div>
                    </div>
                    <div className="youth-col">
                        <div className="col-text">
                            <h4>Case</h4>
                            <hr className="youth-info-divider"/>
                        </div>
                        <div className="inner-col">
                            <p>Case Manager: <span>Linda Cox</span></p>
                            <p>Personal Counselor: <span>Jeff Bridges</span></p>
                            <p>Placement Date: <span>{this.props.currentYouth.placement_date}</span></p>
                            <p>Placement:  
                                <span> {this.props.currentYouth.placement_type.name}
                                    <span> - { this.props.currentYouth.placement_type.default_stay} days</span>
                                </span>
                            </p>
                            <p>Expected Exit: <span>{this.props.currentYouth.expectedExit}</span></p>
                        </div>
                        <div className="inner-col">
                            <p>Referred By: <span>Slam Bam</span></p>
                            <p>Social Worker: <span>Qualm Bomb</span></p>
                            <p>Bed Nights: <span>7</span></p>
                            <p>Where Exited: <span>Parent's Home</span></p>
                            <p>Permanent Housing: <span>Yes</span></p>
                        </div>
                    </div>
                </div>
                <div className="youth-row">
                    <div className="col-text">
                        <h4>School</h4>
                        <hr className="youth-info-divider"/>
                    </div>
                    <div className="inner-col">
                        <p>School: <span>{this.props.currentYouth.school.name}</span></p>
                        <p>District: <span>{this.props.currentYouth.school.district}</span></p>
                        <p>Phone: <span>{this.props.currentYouth.school.phone}</span></p>
                    </div>
                    <div className="inner-col">
                        <p>AM Transport: <span>Bus</span></p>
                        <p>AM Pickup Time: <span>7:45 AM</span></p>
                        <p>AM Phone: <span>5555555555</span></p>
                    </div>
                    <div className="inner-col">
                        <p>PM Transport: <span>Bus</span></p>
                        <p>PM Dropoff Time: <span>3:30 PM</span></p>
                        <p>PM Phone: <span>5555555555</span></p>
                    </div>
                    <div className="inner-col">
                        <p>Date Requested: <span>10/14/2016</span></p>
                        <p>MKV Complete: <span>Yes</span></p>
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


