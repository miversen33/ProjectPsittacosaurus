import React from 'react';
import Cookies from 'js-cookie';
import BaseLayout from './BaseLayout';

class UserForm extends React.Component{
    constructor(props){
        super(props);

        this.state = {
            originalState: {}, 
            newState: {}, 
            sessionid: Cookies.get('sessionid'), 
            userid: Cookies.get('userid'),
            session_type: 'w',
            readyToDisplay: false
        };

        this.getModifyUserInfo = this.getModifyUserInfo.bind(this);
        this.sendModifyUserInfo = this.sendModifyUserInfo.bind(this);
    }

    componentDidMount(){
        this.getModifyUserInfo();
    }

    getModifyUserInfo(){
        var request = JSON.stringify(this.state);
        var authLocation = 'http://localhost:3000/modify_user';
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
            .then(data => {
                this.setState((state) => {
                    // We dont care about the status code
                    return {originalState: {...state.originalState, ...data.fields}};
                }); 
                this.setState((state) => {
                    return {newState: state.originalState}
                })
                this.setState((state) => {return {readyToDisplay: true};})
                console.log(this.state);
                // Also should make the "save changes" or "submit" button visible here so that the page doesn't just have
                // a floating button that moves
            });
    }

    sendModifyUserInfo(){
        var changedData = {irrelevantThing: 'sdfometh'}
        Object.entries(this.state.newState).map(([key, value]) => {
            if(this.state.originalState[key] !== value){
                changedData[key] = value;
            }
        });
        changedData['email_address'] = 'bullshit@email.com';
        changedData['new_password'] = 'password1'
        console.log(changedData);
        var request = {
            fields: {
                ...changedData, 
            },
            password: 'password',
            sessionid: this.state.sessionid, 
            userid: this.state.userid, 
            session_type: this.state.session_type
        }
        console.log(request);
        var authLocation = 'http://localhost:3000/modify_user';
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(request)
        };
        fetch(authLocation, requestOptions)
            .then(response => {
                const contentType = response.headers.get('content-type');
                if (!contentType || !contentType.includes('application/json')) {
                    console.log("Response isn't JSON! I hope you know what you're doing!");
                }
                return response.json();
            })
            // .then(data => {});
    }

    render(){
        return(
            <div>
                {
                    !this.state.readyToDisplay ? null: 
                    <div>

                        {Object.entries(this.state.newState).map(([key, value]) => {
                            return <div>
                                <div>{key}:{value}</div>
                            </div>
                        })}
                        <button onClick={this.sendModifyUserInfo}>Save Changes</button>
                    </div>
                }
                {/* <ul>
                    {Object.entries(this.state.newState).map(([key, value]) => {return <li>{value}</li>})}
                </ul> */}
            </div>
        )
    }


}

function ModifyUser(){
    return (
        <BaseLayout fabDisabled={true}>
            <UserForm></UserForm>
        </BaseLayout>
    );
}



export default ModifyUser;

    // handleSubmit(_){
    //     // TODO(Mike) Encode me! We should fetch an encoding key on document ready, so that the information that is sent out
    //     // is encoded in some way. This only needs to happen for authentication
    //     var request = JSON.stringify({username: this.state.username, password: this.state.password, type: 'web'});
    //     var authLocation = 'http://localhost:3000/login';
    //     const requestOptions = {
    //         method: 'POST',
    //         headers: { 'Content-Type': 'application/json' },
    //         body: request
    //     };
    //     fetch(authLocation, requestOptions)
    //         .then(response => {
    //             const contentType = response.headers.get('content-type');
    //             if (!contentType || !contentType.includes('application/json')) {
    //                 console.log("Response isn't JSON! I hope you know what you're doing!");
    //             }
    //             return response.json();
    //         })
    //         .then(data => {this.handleLoginResponse(data);});
    // }

    // handleLoginResponse(response){
    //     console.log(response);
    //     if(response.status_code === 401){
    //         console.log('Incorrect User Credentials. Flash error');
    //         return;
    //     }
    //     if(response.status_code === 500){
    //         // TODO(Mike): We should probably setup a general landing page for some of these errors
    //         console.log("Server Error. Likely not you're fault, sorry bucko.");
    //         return;
    //     }
    //     if(response.status_code === 404){
    //         console.log("Server says this page doesn't exist. Thats coolio");
    //         return;
    //     }
    //     if(response.status_code === 200){
    //         console.log("Hurray!");
    //         Cookies.set('username', response.username);
    //         Cookies.set('sessionid', response.sessionid);
    //         Cookies.set('userid', response.userid);
    //         // TODO(Mike): Redirect to a general "home" page, after we are logged in
    //         return;
    //     }
    //     console.log("You got some weird ass response bro");
    //     console.log(response);
    // }


    // render(){
    //     return (
    //         <div className="form-group">
    //             <form onSubmit={this.handleSubmit}>
    //                 <input type="text" placeholder='User Name' value={this.state.username} onChange={this.handleChange} name="username"></input>
    //                 <input type="password" placeholder='Password' value={this.state.password} onChange={this.handleChange} name="password"></input>
    //             </form>
    //             <button onClick={this.handleSubmit} className="btn btn-primary">Login!</button>
    //         </div>
    //     );
    // }

// function Login(){

//     return <BaseLayout fabDisabled={true}>
//         <AuthForm></AuthForm>
//     </BaseLayout>
// }

// export default Login;