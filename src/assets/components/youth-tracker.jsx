import React from 'react';
import {Link, IndexLink} from "react-router";
import YouthTrackerRow from "./youth-tracker-row.jsx";
import "whatwg-fetch";

const ALL_YOUTH_API = "/api/youth/?activeOnly=";
let showActive = "true";

let headers = [
            "Name",
            "DOB",
            "Entry Date",
            "Placement",
            "School",
            "School Transport",
            "School Pickup",
            "Form Progress",
            "Planned Exit"
            ];

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
    }

    // getHeaderColumns() {
    //     return ([
    //         "Name",
    //         "DOB",
    //         "Entry Date",
    //         "Placement",
    //         "School",
    //         "School Transport",
    //         "School Pickup",
    //         "Form Progress",
    //         "Planned Exit"
    //     ]);
    // }

    addHeaderColumn(title) {
        headers.push(title)
    }

    buildHeader() {
        // let headers = this.getHeaderColumns();
        let tr = document.querySelector(".header-row");

        if (tr != null) {
            headers.forEach(function(header) {
                let th = document.createElement("th");
                th.textContent = header;
                tr.appendChild(th);
            });
        }
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
            <table className="mdl-data-table mdl-js-data-tabled youth-tracker-container">
                <thead>
                    <tr className="header-row">
                        {this.buildHeader()}
                        {/*<th className="mdl-data-table__cell--non-numeric">Name</th>
                        <th>DOB</th>
                        <th>Entry Date</th>
                        <th>Placement</th>
                        <th>School</th>
                        <th>School Transport</th>
                        <th>School Pickup</th>
                        <th>Form Progress</th>
                        <th>Planned Exit</th>*/}
                    </tr>
                </thead>
                <tbody>
                    {youthData}
                </tbody>
            </table>
        );
    } 
}