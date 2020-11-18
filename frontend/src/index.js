import React from 'react';
import ReactDOM from 'react-dom';
import './static/css/index.css';
import * as serviceWorker from './static/js/serviceWorker';

import Routes from './routes.js';

ReactDOM.render(
  <React.StrictMode>
    <Routes />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();


// import YourComponent from "./path/of/your/component";

//     <Router>
//       <Route exact path="/insert/your/path/here" component={YourComponent} />
//     </Router>

// //The component that has the handleClick function

// import { Link } from "react-router-dom"; 

// class App extends Component {
//   render() {
//      return(
//        <div>
//          <Link to="/insert/your/path/here" className="btn btn-primary">hello</Link>
//       </div>
//      );
//   }
// }