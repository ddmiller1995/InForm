import React from 'react';
import {Link, IndexLink} from "react-router";
import YouthTrackerRow from "./youth-tracker-row.jsx";
import "whatwg-fetch";

const ALL_YOUTH_API = "/api/youth/?activeOnly=";
let showActive = true;

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
        fetch(ALL_YOUTH_API + showActive)
            .then(response => response.json())
            .then(data => this.setState({ youth: data }))
            .catch(err => alert(err.message));

        this.registerActiveOnly();
    }

    getYouthData() {
        let rows;
        if (this.state.youth) { 
            rows = this.state.youth.youth.map(youth => <YouthTrackerRow key={youth.name} youth={youth} />);
        }
        return rows;
    }

    registerActiveOnly() {
        let that = this;
        $("#active-only").change(function() {
            showActive = !showActive;

            fetch(ALL_YOUTH_API + showActive)
                .then(response => response.json())
                .then(data => that.setState({ youth: data }))
                .catch(err => alert(err.message));
        });
    }

    render() {
        let youthData = this.getYouthData();

        return (
            <table className="mdl-data-table mdl-js-data-tabled youth-tracker-container">
                <thead>
                    <tr className="header-row">
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
                        <th>Exit Date</th>
                    </tr>
                </thead>
                <tbody>
                    {youthData}
                </tbody>
            </table>
        );
    } 
}