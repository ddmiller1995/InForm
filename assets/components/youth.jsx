import React from "react";
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }
      
    render() {
        return (
            <div className="container">
                <div className="youth-detail-container">
                    <header className="mdl-layout__header">
                        <div className="mdl-layout__header-row">
                            <nav className="mdl-navigation">
                                <IndexLink className="mdl-navigation__link" to="/youth" activeClassName="active">Personal File</IndexLink>
                                <div className="header-divider"></div>
                                <IndexLink className="mdl-navigation__link" to="/youth/progress" activeClassName="active">Progress Chart</IndexLink>
                                <div className="header-divider"></div>
                                <IndexLink className="mdl-navigation__link" to="/youth/forms" activeClassName="active">Forms</IndexLink>
                            </nav>
                        </div>
                    </header>
                    <hr className="youth-detail-divider"/>
                    <h4>details here</h4>
                </div>
            </div>
        );
    }
}