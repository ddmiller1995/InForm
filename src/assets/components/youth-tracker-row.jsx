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
                <td>11/12/2001</td>
                <td>2/13/2017</td>
                <td>Progress</td>
                <td>Progress</td>
                <td>Progress</td>
                <td>3/2/2017</td>
            </tr>
        );
    } 
}