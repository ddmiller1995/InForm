import React from 'react';
import {Link, IndexLink} from "react-router";
import YouthTrackerRow from "./youth-tracker-row.jsx";
import { getRequest } from '../util.js'
import "whatwg-fetch";

const ALL_YOUTH_API = "/api/youth/?activeOnly=";
const TRACKER_FIELDS_API = "/api/youth-tracker-field-list/"
let showActive = true;

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
        let data = getRequest(ALL_YOUTH_API + showActive, this, "youth");
        getRequest(TRACKER_FIELDS_API, this, "fields");
        this.registerActiveOnly();
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
            if(headers.length > 0) {
                headers.push(<th key='Exit date'>Exit Date</th>);
            } else {
                headers.push(<th key={0}></th>);
            }
        }
        return headers;
    }

    registerActiveOnly() {
        let that = this;
        $("#active-only").change(function() {
            showActive = !showActive;
            let data = getRequest(ALL_YOUTH_API + showActive, that, "youth");
        });
    }

    render() {
        let youthData = this.getYouthData();
        let fieldData = this.getFields();

        return (
            <table className="mdl-data-table mdl-js-data-tabled youth-tracker-container">
                <thead>
                    <tr className="header-row">
                        {fieldData}
                    </tr>
                </thead>
                <tbody>
                    {youthData}
                </tbody>
            </table>
        );
    } 
}