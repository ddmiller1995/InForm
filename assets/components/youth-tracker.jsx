import React from 'react';
import ReactDOM from 'react-dom';
import "whatwg-fetch";

export default class YouthTracker extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    // table data is hard coded for now, but rows will likely become separate components rendered dynamically
    render() {
        return (
            <div className="youth-tracker-container">
                <table className="mdl-data-table mdl-js-data-tabled">
                    <thead>
                        <tr>
                            <th class="mdl-data-table__cell--non-numeric">Name</th>
                            <th>DOB</th>
                            <th>Entry Date</th>
                            <th>Intake Forms</th>
                            <th>Outtake Forms</th>
                            <th>Case Goals</th>
                            <th>Planned Exit</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="mdl-data-table__cell--non-numeric">John Smith</td>
                            <td>11/12/2001</td>
                            <td>2/13/2017</td>
                            <td>Progress</td>
                            <td>Progress</td>
                            <td>Progress</td>
                            <td>3/2/2017</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        );
    } 
}