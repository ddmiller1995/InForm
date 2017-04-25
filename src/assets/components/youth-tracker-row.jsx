import React from 'react';
import {store, setCurrentYouth} from "./shared-state.js";
import {Link, IndexLink} from "react-router";
import { formatDate, formatTime, registerDialog } from '../util.js'
import "whatwg-fetch";

var moment = require("moment");

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

    toggleModal() {
        let div = this.buildDialog();
        // if dialog doesn't exist, append it
        if (document.getElementById("mdl-dialog") == null) {
            document.querySelector(".youth-tracker-container").appendChild(div.firstElementChild);
        } 
        // @param1: parent container that dialog child will be added and removed from
        // @param2: index of dialog in childNodes array
        registerDialog(".youth-tracker-container", 2);
    }

    buildDialog() {
        let div = document.createElement("div"); 
        let today = moment().format("YYYY-MM-DD");
        let modal = (`
            <dialog id="mdl-dialog" className="exit-dialog">
                <h4 id="dialog-title">Mark ${this.props.youth.name} exited</h4>
                <div id="exit-warning">
                    <p>
                        <i>Only mark a youth as exited if they have left the shelter. For extending stays 
                        or changing beds, please go <a href="#youth">here</a></i>
                    </p>
                </div>
                <div id="dialog-descr">
                    <p>Exit Date: <span><input id="date-input" type="date" value=`+today+`></input></span></p>
                    <p>Where did they exit to? <span><input id="exited-to-input" type="text"></input></span></p>
                    <p>Permanent Housing? 
                        <span> 
                         <input id="yes-checkbox" name="housing" type="radio" value="true"></input>Yes 
                         <input id="no-checkbox" name="housing" type="radio" value="false"></input>No 
                         <input id="unknown-checkbox" name="housing" type="radio" value="null"></input>Unknown 
                        </span>
                    </p>
                </div>
                <div id="dialog-actions">
                    <button type="button" id="dialog-submit">Save</button>
                    <button type="button" id="dialog-close">Cancel</button>
                </div>
            </dialog>
        `);

        div.innerHTML = modal;
        return div;
    }

    render() {
        // show AM school info 12AM-11:59AM, otherwise show PM
        let hour = new Date().getHours();
        let pickupTime = this.props.youth.school_am_pickup_time;
        let transport = this.props.youth.school_am_transport;
        if (hour >= 12) {
            pickupTime = this.props.youth.school_pm_dropoff_time;
            transport = this.props.youth.school_pm_transport;
        }

        let currentPlacement = this.props.youth.current_placement_type;

        return (
            <tr>
                <td className="mdl-data-table__cell--non-numeric">{this.wrapIndexLink(this.props.youth.name)}</td>
                <td>{this.wrapIndexLink(formatDate(this.props.youth.dob))}</td>
                <td>{this.wrapIndexLink(formatDate(this.props.youth.visit_start_date))}</td>
                <td>{this.wrapIndexLink(currentPlacement[currentPlacement.length - 1].name)}</td>
                <td>{this.wrapIndexLink(this.props.youth.school.school_name)}</td>
                <td>{this.wrapIndexLink(transport)}</td>
                <td>{this.wrapIndexLink(formatTime(pickupTime))}</td>
                <td>{this.wrapIndexLink(this.props.youth.overall_form_progress)}</td>
                <td>{this.wrapIndexLink(formatDate(this.props.youth.estimated_exit_date))}</td>
                <td className="exit-column">
                    {this.props.visit_exit_date ||
                    <button className="mdl-button mdl-js-button add-exit" onClick={() => this.toggleModal()}>
                        <i className="material-icons add-exit-icon">add</i>Add
                    </button>}
                </td>
            </tr>
        );
    } 
}