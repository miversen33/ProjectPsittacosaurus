import React from 'react';
import Cookies from 'js-cookie';
import BaseLayout from './BaseLayout';

class AuthForm extends React.Component{
    constructor(props){
        super(props);
        this.state = {username: '', password: ''};

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

        Cookies.remove('username');
        Cookies.remove('sessionid');
        Cookies.remove('userid');
    }

    handleChange(event){
        var key = event.target.name;
        this.setState({[key]: event.target.value});
    }

    handleSubmit(_){
        // TODO(Mike) Encode me! We should fetch an encoding key on document ready, so that the information that is sent out
        // is encoded in some way. This only needs to happen for authentication
        var request = JSON.stringify({username: this.state.username, password: this.state.password, session_type: 'web'});
        var authLocation = 'http://localhost:3000/login';
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: request
        };
        fetch(authLocation, requestOptions)
            .then(response => {
                const contentType = response.headers.get('content-type');
                if (!contentType || !contentType.includes('application/json')) {
                    console.log("Response isn't JSON! I hope you know what you're doing!");
                }
                return response.json();
            })
            .then(data => {this.handleLoginResponse(data);});
    }

    handleLoginResponse(response){
        console.log(response);
        if(response.status_code === 401){
            console.log('Incorrect User Credentials. Flash error');
            return;
        }
        if(response.status_code === 500){
            // TODO(Mike): We should probably setup a general landing page for some of these errors
            console.log("Server Error. Likely not you're fault, sorry bucko.");
            return;
        }
        if(response.status_code === 404){
            console.log("Server says this page doesn't exist. Thats coolio");
            return;
        }
        if(response.status_code === 200){
            // console.log("Hurray!");
            // Cookies.set('username', response.username);
            // Cookies.set('sessionid', response.sessionid);
            // Cookies.set('userid', response.userid);
            // TODO(Mike): Redirect to a general "home" page, after we are logged in
            return;
        }
        console.log("You got some weird ass response bro");
        console.log(response);
    }


    render(){
        return (
            <div className="form-group">
                <form onSubmit={this.handleSubmit}>
                    <input type="text" placeholder='User Name' value={this.state.username} onChange={this.handleChange} name="username"></input>
                    <input type="password" placeholder='Password' value={this.state.password} onChange={this.handleChange} name="password"></input>
                </form>
                <button onClick={this.handleSubmit} className="btn btn-primary">Login!</button>
            </div>
        );
    }
}
function Login(){

    return <BaseLayout fabDisabled={true}>
        <AuthForm></AuthForm>
    </BaseLayout>
}

export default Login;