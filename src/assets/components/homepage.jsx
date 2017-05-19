import React from "react";
import {Link, IndexLink} from "react-router";
import YouthTracker from "./youth-tracker.jsx";
import "whatwg-fetch";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            checked: true
        };
    }

    toggleCheckbox() {
        this.setState({
            checked: !this.state.checked
        })
    }
      
    render() {
        let isChecked = this.state.checked ? "checked" : "";

        return (
            <div className="youth-tracker-container">
                <header className="mdl-layout__header">
                    <div className="mdl-layout__header-row header-fix">
                            <nav className="mdl-navigation homepage-bar">
                                <a href="#presentation" className="mdl-navigation__link presentation-link"><i className="material-icons present-icon">tv</i>Presentation View</a>
                                <div id="show-active">
                                    <input id="active-only" type="checkbox" onChange={() => this.toggleCheckbox()} checked={this.state.checked}></input>
                                    <label htmlFor="active-only">Show active</label>
                                </div>
                                <div className="add-youth">
                                    <a className="mdl-navigation__link" href="/admin/api/youthvisit/add/">
                                        <i className="material-icons">add</i>
                                        Add Youth
                                    </a>
                                </div>
                            </nav>
                        </div>
                </header>

                <YouthTracker />
            </div>
        );
    }
 }