a = window.location.href.split("=")[1];
if (a) {
  var token = a.slice(0, -11);//slices exacly the token
  sessionStorage.setItem("token", token);
  console.log(token);
};
