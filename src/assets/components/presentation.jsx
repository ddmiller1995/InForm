import React from 'react';
import {Link, IndexLink} from "react-router";
import { getRequest } from '../util.js'
import YouthTrackerRow from "./youth-tracker-row.jsx";
import "whatwg-fetch";

const ALL_YOUTH_API = "/api/youth/?activeOnly=true";
const TRACKER_FIELDS_API = "/api/youth-tracker-field-list/"

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
        let data = getRequest(ALL_YOUTH_API, this, "youth");
        getRequest(TRACKER_FIELDS_API, this, "fields");

    }

    getYouthData() {
        let rows;
        if (this.state.youth && this.state.fields) { 
            rows = this.state.youth.youth.map(youth => <YouthTrackerRow key={youth.name} youth={youth} fields={this.state.fields.fields} />);
        }
        return rows;
    }

    getFields() {
        let headers;
        if(this.state.fields) {
            headers = this.state.fields.fields.map(field => <th key={field.field_name} >{field.field_name}</th>);
        }
        return headers;
    }

    render() {
        let youthData = this.getYouthData();
        let fieldData = this.getFields();

        return (
            <div>
                <button className="mdl-button mdl-js-button exit-btn">
                    <IndexLink className="mdl-navigation__link" to="/" activeClassName="active">
                        <i className="material-icons exit-icon">clear</i>
                    </IndexLink>
                </button>
                <table className="mdl-data-table mdl-js-data-tabled presentation-container">
                    <div className="overlay"></div>
                    <thead>
                        <tr>
                            {fieldData}
                        </tr>
                    </thead>
                    <tbody>
                        {youthData}
                    </tbody>
                </table>
            </div>
        );
    } 
}