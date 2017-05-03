import React from 'react';
import {Link, IndexLink} from "react-router";
import { getRequest } from '../util.js'
import YouthTrackerRow from "./youth-tracker-row.jsx";
import "whatwg-fetch";

const ALL_YOUTH_API = "/api/youth/?activeOnly=true";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
        let data = getRequest(ALL_YOUTH_API, this, "youth");
    }

    getYouthData() {
        let rows;
        if (this.state.youth) { 
            rows = this.state.youth.youth.map(youth => <YouthTrackerRow key={youth.name} youth={youth} />);
        }
        return rows;
    }

    render() {
        let youthData = this.getYouthData();

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
                            <th className="mdl-data-table__cell--non-numeric">Name</th>
                            <th>DOB</th>
                            <th>Entry Date</th>
                            <th>Placement</th>
                            <th>School</th>
                            <th>AM Transport</th>
                            <th>PM Transport</th>
                            <th>AM Pickup/PM Dropoff</th>
                            <th>Form Progress</th>
                            <th>Estimated Exit</th>
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