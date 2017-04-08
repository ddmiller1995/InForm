import React from "react";
import {store} from "./shared-state.js";
import {Link, IndexLink} from "react-router";
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
                    <main>
                        {React.cloneElement(this.props.children, {currentYouth: this.state.currentYouth})}
                    </main>
                </div>
            </div>
        );
    }
}
