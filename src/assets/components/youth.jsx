import React from "react";
import {store} from "./shared-state.js";
import {Link, IndexLink} from "react-router";
import "whatwg-fetch";

const GET_YOUTH_API = "/api/youth/"
const YOUTH_ID = store.getState();

export default class extends React.Component {
    constructor(props) {
        super(props);
        this.state = {youth: {}};
    }

     componentDidMount() {
        this.unsub = store.subscribe(() => this.setState(store.getState()));

        fetch(GET_YOUTH_API + YOUTH_ID.currentYouth.id)
            .then(response => response.json())
            .then(data => this.setState({ youth: data }))
            .catch(err => alert(err.message));
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
                            </nav>
                        </div>
                    </header>
                    <hr className="youth-detail-divider"/>
                    <main>
                        {React.cloneElement(this.props.children, {currentYouth: this.state.youth})}
                    </main>
                </div>
            </div>
        );
    }
}
