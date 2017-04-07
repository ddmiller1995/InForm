import React from 'react';
import {store, setCurrentYouth} from "./shared-state.js";
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
            <tr>
                <td className="mdl-data-table__cell--non-numeric">
                    <IndexLink 
                        className="mdl-navigation__link" 
                        to="/youth"
                        key={this.props.youth.name} 
                        onClick={() => store.dispatch(setCurrentYouth(this.props.youth))}>
                        {this.props.youth.name}
                    </IndexLink>
                </td>
                <td>{this.props.youth.dob}</td>
                <td>{this.props.youth.placement_date}</td>
                <td>---</td>
                <td>---</td>
                <td>---</td>
            </tr>
        );
    } 
}