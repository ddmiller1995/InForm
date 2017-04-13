import React from "react";
import {Link, IndexLink} from "react-router";
import { formatDate, getDateDiff } from '../util.js'
import "whatwg-fetch";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }
      
    render() {
        return (
            <div className="container youth-info-container">
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
                    </div>
                </div>
                <div className="youth-row">
                    <div className="col-text">
                        <h4>School</h4>
                        <hr className="youth-info-divider"/>
                        <p>School: <span>{this.props.currentYouth.school.name}</span></p>
                        <p>District: <span>{this.props.currentYouth.school.district}</span></p>
                        <p>Phone: <span>{this.props.currentYouth.school.phone}</span></p>
                    </div>
                </div>

                {/*<button className="mdl-button mdl-js-button mdl-button--fab">
                    <i className="material-icons">add</i>
                </button>*/}
            </div>
        );
    }
}


