import React from "react";
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";
import "../css/main.css";

export default class extends React.Component {
    constructor(props) {
          super(props);
    }

    render() {
        if (this.props.location.pathname === "/presentation") {
            return (
                <div>
                    <main>
                        {this.props.children}
                    </main>
                </div>
            );
        }

        return (
            <div className="mdl-layout mdl-js-layout mdl-layout--fixed-header">
                <header className="mdl-layout__header">
                    <div className="mdl-layout__header-row header-fix">
                        {/*<span className="mdl-layout-title">Youth Haven Portal</span>*/}
                        <a className="mdl-navigation__link navbar-logo" href="#"><img className="navbar-logo" href="#" src="/static/components/img/informlogo.png" alt="Inform"/></a>
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
