import React from "react";
import {Link, IndexLink} from "react-router";
import YouthTracker from "./youth-tracker.jsx";
import "whatwg-fetch";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }
      
    render() {
        return (
            <div className="container">
                {/*<div className="homepage-links">
                    <IndexLink className="progress-link" to="/progress" activeClassName="active">Progress Report</IndexLink>
                    <a href="#presentation" className="presentation-link">Presentation View</a>
                </div>

                <div className="add-youth-btn">
                    <a className="mdl-navigation__link" href="/admin/api/youthvisit/add/">
                        <i className="material-icons">add</i>
                        Add Youth
                    </a>
                </div>*/}
                <header className="mdl-layout__header">
                    <div className="mdl-layout__header-row header-fix">
                            <nav className="mdl-navigation homepage-bar">
                                <IndexLink className="mdl-navigation__link progress-link" to="/progress" activeClassName="active">Progress Report</IndexLink>
                                <div className="header-divider"></div>
                                <a href="#presentation" className="mdl-navigation__link presentation-link">Presentation View</a>
                                <div className="add-youth">
                                    <a className="mdl-navigation__link" href="/admin/api/youthvisit/add/">
                                        <i className="material-icons">add</i>
                                        Add Youth
                                    </a>
                                </div>
                            </nav>
                        </div>
                    <div className="">
                        
                    </div>
                </header>

                <YouthTracker />
            </div>
        );
    }
 }