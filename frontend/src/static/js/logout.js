import Cookies from 'js-cookie';

export function logout(){
    var request = JSON.stringify();
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: request
    };

    var requestLocation = 'http://localhost:3000/logout  ';
    fetch(requestLocation, requestOptions)
        .then(response => {
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                console.log("Response isn't JSON! I hope you know what you're doing!");
            }
            return response.json();
        })
        .then(data => {});
}