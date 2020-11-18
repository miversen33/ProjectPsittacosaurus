import React from 'react';

import BaseLayout from './BaseLayout'

class NewUserForm extends React.Component{
    constructor(props){
        super(props);
        this.state = {username: '', password: '', email_address: ''};

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event){
        var key = event.target.name;
        this.setState({[key]: event.target.value});
    }

    handleSubmit(_){
        // TODO(Mike) Encode me! We should fetch an encoding key on document ready, so that the information that is sent out
        // is encoded in some way. This only needs to happen for authentication
        var request = JSON.stringify({username: this.state.username, password: this.state.password, email_address: this.state.email_address});
        var authLocation = 'http://localhost:3000/new_user';
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: request
        };
        fetch(authLocation, requestOptions);
            // .then(response => response.json());
            // .then(data => this.setState({ postId: data.id }));
    }
    //     fetch('http://localhost:3000/authenticate');
    //     console.log(request);
    // }

//     <form>
//   <div class="form-group">
//     <label for="exampleInputEmail1">Email address</label>
//     <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email">
//     <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
//   </div>
//   <div class="form-group">
//     <label for="exampleInputPassword1">Password</label>
//     <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password">
//   </div>
//   <div class="form-check">
//     <input type="checkbox" class="form-check-input" id="exampleCheck1">
//     <label class="form-check-label" for="exampleCheck1">Check me out</label>
//   </div>
//   <button type="submit" class="btn btn-primary">Submit</button>
// </form>
    render(){
        return (
            <div className="form-group">
                <form onSubmit={this.handleSubmit}>
                    <input type="text" placeholder='User Name' value={this.state.username} onChange={this.handleChange} name="username"></input>
                    <input type="password" placeholder='Password' value={this.state.password} onChange={this.handleChange} name="password"></input>
                    <input type="text" placeholder='Email Address' value={this.state.email_address} onChange={this.handleChange} name="email_address"/>
                </form>
                <button onClick={this.handleSubmit} className="btn btn-primary">Create New User</button>
            </div>
        );
    }
}

function NewUser(){
    return <BaseLayout fabDisabled={true}>
        <NewUserForm></NewUserForm>
    </BaseLayout>
}

export default NewUser;