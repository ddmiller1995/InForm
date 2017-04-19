import React from 'react';
import {Link, IndexLink} from "react-router";
import YouthTrackerRow from "./youth-tracker-row.jsx";
import "whatwg-fetch";

const ALL_YOUTH_API = "/api/youth/";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
        fetch(ALL_YOUTH_API)
            .then(response => response.json())
            .then(data => this.setState({ youth: data }))
            .catch(err => alert(err.message));
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
                <button className="mdl-button mdl-js-button">
                    <IndexLink className="mdl-navigation__link" to="/" activeClassName="active">Close</IndexLink>
                </button>
                <table className="mdl-data-table mdl-js-data-tabled presentation-container">
                    <div className="overlay"></div>
                    <thead>
                        <tr>
                            <th className="mdl-data-table__cell--non-numeric">Name</th>
                            <th>DOB</th>
                            <th>Entry Date</th>
                            <th>School</th>
                            <th>School Transport</th>
                            <th>School Pickup</th>
                            <th>Intake Forms</th>
                            <th>Outtake Forms</th>
                            <th>Planned Exit</th>
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