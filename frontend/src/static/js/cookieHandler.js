// cookieExpires is defaulted to 30 days. Please set cookieExpires in increments of days
export function setCookie(cookieName, cookieValue, cookieExpires=30){
    var d = new Date();
    d.setTime(d.getTime()+ cookieExpires*24*60*60*1000);
    cookieExpires = d.toUTCString();
    document.cookie = `${cookieName}=${cookieValue};${cookieExpires};sameSite=strict;path=/`;
}

export function getCookie(cookie){
    var name = cookie + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
        return c.substring(name.length, c.length);
        }
    }
    return "";
}

export function deleteCookie(cookie){
    document.cookie = `${cookie}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}