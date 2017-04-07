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
            <div className="container">
                <h4>{this.props.currentYouth.name}</h4>
                <hr className="youth-info-divider"/>
                <p>Birthdate: <span>{formatDate(this.props.currentYouth.dob)}</span></p>
                <p>Age at Entry: 
                    <span>
                        {getDateDiff(this.props.currentYouth.placement_date, this.props.currentYouth.dob)}
                    </span>
                </p>
                <p>Ethnicity: <span>{this.props.currentYouth.ethnicity}</span></p>
                <p>City: <span>{this.props.currentYouth.city_of_origin}</span></p>
                <h4>Visit Details</h4>
                <hr className="youth-info-divider"/>
                <p>Many other details we don't have yet</p>
            </div>
        );
    }
}


