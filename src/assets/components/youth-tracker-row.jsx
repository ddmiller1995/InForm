import React from 'react';
import {store, setCurrentYouth} from "./shared-state.js";
import {Link, IndexLink} from "react-router";
import { formatDate, formatTime } from '../util.js'
import "whatwg-fetch";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = store.getState();
    }

    componentDidMount() {
        this.unsub = store.subscribe(() => this.setState(store.getState()));
    }

    componentWillUnmount() {
        this.unsub();
    }

    wrapIndexLink(data) {
        return (
            <IndexLink 
                className="mdl-navigation__link" 
                to="/youth"
                key={data} 
                onClick={() => store.dispatch(setCurrentYouth(this.props.youth))}>
                {data}
            </IndexLink>
        );
    }

    render() {
        let hour = new Date().getHours();
        let pickupTime = this.props.youth.school_am_pickup_time;
        let transport = this.props.youth.school_am_transport;
        if (hour >= 12) {
            pickupTime = this.props.youth.school_pm_dropoff_time;
            transport = this.props.youth.school_pm_transport;
        }

        return (
            <tr>
                <td className="mdl-data-table__cell--non-numeric">{this.wrapIndexLink(this.props.youth.name)}</td>
                <td>{this.wrapIndexLink(formatDate(this.props.youth.dob))}</td>
                <td>{this.wrapIndexLink(formatDate(this.props.youth.visit_start_date))}</td>
                <td>{this.wrapIndexLink(this.props.youth.current_placement_type.name)}</td>
                <td>{this.wrapIndexLink(this.props.youth.school.school_name)}</td>
                <td>{this.wrapIndexLink(transport)}</td>
                <td>{this.wrapIndexLink(formatTime(pickupTime))}</td>
                <td>{this.wrapIndexLink(this.props.youth.overall_form_progress)}</td>
                <td>{this.wrapIndexLink(formatDate(this.props.youth.estimated_exit_date))}</td>
            </tr>
        );
    } 
}