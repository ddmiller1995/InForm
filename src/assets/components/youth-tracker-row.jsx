import React from 'react';
import {store, setCurrentYouth} from "./shared-state.js";
import {Link, IndexLink} from "react-router";
import { formatDate, getDateDiff } from '../util.js'
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
                <td>{formatDate(this.props.youth.dob)}</td>
                <td>{formatDate(this.props.youth.placement_date)}</td>
                <td>Seattle School District</td>
                <td>School Bus</td>
                <td>7:45 AM</td>
                <td>Progress</td>
                <td>Progress</td>
                <td>Progress</td>
            </tr>
        );
    } 
}