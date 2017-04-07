import React from 'react';
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
            <div className="youth-tracker-container">
                <table className="mdl-data-table mdl-js-data-tabled">
                    <thead>
                        <tr>
                            <th className="mdl-data-table__cell--non-numeric">Name</th>
                            <th>DOB</th>
                            <th>Entry Date</th>
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