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

    wrapIndexLink(data) {
        return (
            <IndexLink 
                className="mdl-navigation__link" 
                to="/youth"
                key={data} 
                onClick={() => store.dispatch(setCurrentYouth(this.props.youth))}>
                {data}
            </IndexLink>
        );
    }

    render() {
        return (
            <tr>
                <td className="mdl-data-table__cell--non-numeric">{this.wrapIndexLink(this.props.youth.name)}</td>
                <td>{this.wrapIndexLink(formatDate(this.props.youth.dob))}</td>
                <td>{this.wrapIndexLink(formatDate(this.props.youth.placement_date))}</td>
                <td>{this.wrapIndexLink(this.props.youth.placement_type.name)}</td>
                <td>{this.wrapIndexLink("Seattle School District")}</td>
                <td>{this.wrapIndexLink("School Bus")}</td>
                <td>{this.wrapIndexLink("7:45 AM")}</td>
                <td>{this.wrapIndexLink("Progress")}</td>
                <td>{this.wrapIndexLink(this.props.youth.expectedExit)}</td>
            </tr>
        );
    } 
}