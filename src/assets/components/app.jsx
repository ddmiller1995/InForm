import React from "react";
import {Link, IndexLink} from "react-router";
// import {store} from "./shared-state.js";
import "whatwg-fetch";
import "../css/main.css";

export default class extends React.Component {
    constructor(props) {
          super(props);
        //   this.state = store.getState();
    }

    // componentDidMount() {
    //     this.unsub = store.subscribe(() => this.setState(store.getState()));
    // }

    // componentWillUnmount() {
    //     this.unsub();
    // }

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
                            <IndexLink className="mdl-navigation__link" to="/admin" activeClassName="active">Admin</IndexLink>
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
