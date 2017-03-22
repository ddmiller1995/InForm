import React from "react";
import {render} from "react-dom";
import {AppContainer} from 'react-hot-loader';

import App from "./components/app.jsx";

ReactDOM.render(<AppContainer><App/></AppContainer>, document.getElementById("app"));
