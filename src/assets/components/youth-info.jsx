import React from "react";
import {Link, IndexLink} from "react-router";
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
                <p>DOB: <span>{this.props.currentYouth.DOB}</span></p>
                <p>Age at Entry: <span>{this.props.currentYouth.entryDate} - {this.props.currentYouth.DOB}</span></p>
                <p>Ethnicity: <span>{this.props.currentYouth.ethnicity}</span></p>
                <p>City: <span>{this.props.currentYouth.city}</span></p>
                <h4>Visit Details</h4>
                <hr className="youth-info-divider"/>
                <p>Many other details we don't have yet</p>
            </div>
        );
    }
}
