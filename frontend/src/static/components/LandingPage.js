import React from 'react';
import BaseLayout from './BaseLayout';
import {logout} from '../js/logout';
import 'bootstrap/dist/css/bootstrap.css';
import '../css/App.css';

function LandingPage(){
  return (
    <BaseLayout fab_location='top-right' fabOnClick={logout}>
    </BaseLayout>
  );
}

// function sendTest(){
//   var authLocation = 'http://localhost:3000/test';
//   // const requestOptions = {
//   //     method: 'GET',
//   //     headers: { 'Content-Type': 'application/json' }
//   // };
//   fetch(authLocation);
// }

export default LandingPage;
