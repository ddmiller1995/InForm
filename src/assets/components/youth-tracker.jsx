import React from 'react';
// import {store} from "./shared-state.js";
import YouthTrackerRow from "./youth-tracker-row.jsx";
import "whatwg-fetch";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
        let data = [{
            name: "John Smith",
            DOB: "11/12/2001",
            entryDate: "2/13/2017",
            intakeProgress: "Progress",
            outtakeProgress: "Progress",
            caseGoalProgress: "Progress",
            expectedExit: "3/2/2017"
        }];

        this.setState({
            youth: data
        });
    }

    // handleYouthNameClick(youth) {
    //     console.log("clicked on " + youth.name);
    // }

    getYouthData() {
        let rows;
        if (this.state.youth) { 
            rows = this.state.youth.map(youth => <YouthTrackerRow key={youth.name} youth={youth} />);
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
                            <th>Case Goals</th>
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