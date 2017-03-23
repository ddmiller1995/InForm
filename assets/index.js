import React from "react";
import {AppContainer} from 'react-hot-loader';
import {render} from "react-dom";

import App from "./components/app.jsx";

render(<AppContainer><App/></AppContainer>, document.getElementById("app"));
