function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function afficher(reponse) {
    console.log(reponse);
}

/* Generic asynchronous Get request*/
function zajaxGet(url, callback) {

    let request = new XMLHttpRequest();

    request.open("GET", url);

    request.addEventListener("load", function() {
        if (request.status >= 200 && request.status < 400) {

            /* reply of the request */
            callback(request.responseText);
        } else {
            console.error(request.status + " " + request.statusText + " " + url);
        }
    });
    request.addEventListener("error", function() {
        console.error("Erreur réseau avec l'URL " + url);
    });
    request.send(null);
}

/* Generic asynchronous Post request*/
function zajaxPost(url, data, callback, callback_sync, isJson) {

    var csrftoken = getCookie('csrftoken');
    // var csrftoken = Cookies.get('csrftoken');

    let request = new XMLHttpRequest();

    request.open("POST", url);
    // request.setRequestHeader("XSRF-TOKEN", csrftoken);
    request.setRequestHeader("X-CSRFToken", csrftoken);

    request.addEventListener("load", function() {

        // signal response is received
        callback_sync();
        if (request.status >= 200 && request.status < 400) {

            callback(request.responseText);
        } else {
            console.error(request.status + " " + request.statusText + " " + url);
        }
    });

    request.addEventListener("error", function() {
        // signal response is received
        callback_sync();
        console.error("Erreur réseau avec l'URL " + url);
    });

    if (isJson) {
        req.setRequestHeader("Content-Type", "application/json");
        data = JSON.stringify(data);
    }

    request.send(data);
}