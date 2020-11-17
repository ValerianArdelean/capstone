a = window.location.href.split("=")[1];
if (a) {
  var token = a.slice(0, -11);//slices exacly the token
  sessionStorage.setItem("token", token);
};

var a = document.getElementById('post_provider');
a.onsubmit = function(e) {
  e.preventDefault();
  token = sessionStorage.getItem("token");
  fetch('/providers', {
    method : 'PUT',
    headers : {"Authorization": "Bearer " + token, "Content-Type":"application/json"}
  })
  .then(respond => respond.json())
  .then(jsonRespond => {
    if (jsonRespond.success) {
      window.location.href = jsonRespond.redirect;
    } else {
      alert('you not authorize');
    };
  });
};

var a = document.getElementById('post_customer');
a.onsubmit = function(e) {
  e.preventDefault();
  token = sessionStorage.getItem("token");
  fetch('/customers', {
    method : 'PUT',
    headers : {"Authorization": "Bearer " + token, "Content-Type":"application/json"}
  })
  .then(respond => respond.json())
  .then(jsonRespond => {
    if (jsonRespond.success) {
      window.location.href = jsonRespond.redirect
    } else {
      alert('you not authorize')
    }
  });
};

a = document.getElementById('logout')
a.onclick = function() {
  sessionStorage.removeItem("token");
}

logs = document.getElementById('logs')
token = sessionStorage.getItem("token");
if (token) {
  console.log(token);
  logs.innerHTML = 'Welcome, you are logged in !'
} else {
  logs.innerHTML = 'Welcome guest !'
}
