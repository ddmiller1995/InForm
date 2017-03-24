import React from 'react';
import ReactDOM from 'react-dom';
import {Table, Column, Cell} from 'fixed-data-table';
import "whatwg-fetch";

// Table data as a list of array.
const rows = [
    ['a1', 'b1', 'c1'],
    ['a2', 'b2', 'c2'],
    ['a3', 'b3', 'c3'],
];

export default class YouthTracker extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <div className="youth-tracker-container">
                <table className="youth-tracker">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Price</th>
                        </tr>
                    </thead>
                    <tbody>Youth</tbody>
                </table>
            </div>
        );
    }

    /*render() {
        return (
            <Table
                rowHeight={50}
                rowsCount={rows.length}
                width={500}
                height={700}
                headerHeight={50}>
                <Column
                    header={<Cell>Col 1</Cell>}
                    cell={<Cell>Column 1 static content</Cell>}
                    width={2000}
                />
                <Column
                    header={<Cell>Col 2</Cell>}
                    cell={<Cell>Column 2 static content</Cell>}
                    width={1000}
                />
                <Column
                    header={<Cell>Col 3</Cell>}
                    cell={<Cell>Column 3 static content</Cell>}
                    width={2000}
                />
            </Table>
        )
    }*/
}