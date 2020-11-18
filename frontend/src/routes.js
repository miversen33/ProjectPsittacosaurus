import React from 'react';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';

import Login from './static/components/Login';
import LandingPage from './static/components/LandingPage'
import NewUser from './static/components/NewUser';
import ModifyUser from './static/components/ModifyUser';

export default() => (
    <Router>
        <Switch>
            <Route exact path="/" component={LandingPage}/>
            <Route path="/login" component={Login}/>
            <Route path="/new_user" component={NewUser}/>
            <Route path="/modify_user" component={ModifyUser}/>
        </Switch>
    </Router>
);
// import YourComponent from "./path/of/your/component";


//     <Router>
//       <Route exact path="/insert/your/path/here" component={YourComponent} />
//     </Router>


// Routes.js

// export default () => (
// <BrowserRouter>
//     <Switch>
//       <Route exact path="/" component={CryptoList}/>
//       <Route path="/currency" component={Currency}/>
//     </Switch>
// </BrowserRouter>
// );