import React from 'react';
import ReactDOM from 'react-dom';
import "whatwg-fetch";

export default class YouthTracker extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <div className="youth-tracker-container">
                <table className="youth-tracker">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>DOB</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>John Smith</td>
                            <td>11/12/2001</td>
                        </tr> 
                    </tbody>
                </table>
            </div>
        );
    } 
}