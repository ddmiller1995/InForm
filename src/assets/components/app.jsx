import React from "react";
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";
import "../css/main.css";

export default class extends React.Component {
    constructor(props) {
          super(props);
    }

    render() {
        return (
            <div className="mdl-layout mdl-js-layout mdl-layout--fixed-header">
                <header className="mdl-layout__header">
                    <div className="mdl-layout__header-row">
                        <span className="mdl-layout-title">Youth Haven Portal</span>
                        <div className="mdl-layout-spacer"></div>
                        <nav className="mdl-navigation">
                            <IndexLink className="mdl-navigation__link" to="/" activeClassName="active">Home</IndexLink>
                            <div className="header-divider"></div>
                            <a className="mdl-navigation__link" href="/admin">Admin</a>
                            <div className="header-divider"></div>
                            <a className="mdl-navigation__link" href="#">Logout</a>
                        </nav>
                    </div>
                </header>
                <main>
                    {this.props.children}
                </main>
            </div>
        );
    }
 }
