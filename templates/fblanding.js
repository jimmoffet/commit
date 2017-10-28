
var uid = '';
var shortToken = '';
var tmpresponse;
var longToken = '';

window.fbAsyncInit = function() {
  FB.init({
    appId      : '2024489881171070',
    cookie     : true,  // enable cookies to allow the server to access 
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.8' // use graph api version 2.8
  });

  function logoutFacebook()
  {
      FB.getLoginStatus(function(response) {
          if (response.status === 'connected') {
            // the user is logged in and has authenticated your
            // app, and response.authResponse supplies
            // the user's ID, a valid access token, a signed
            // request, and the time the access token 
            // and signed request each expire
            var uid = response.authResponse.userID;
            var accessToken = response.authResponse.accessToken;

            FB.api('/'+uid+'/permissions', 'delete', function(response){});

            window.location = "https://commitweb.herokuapp.com";

          } else if (response.status === 'not_authorized') {
            // the user is logged in to Facebook, 
            // but has not authenticated your app
            window.location = "https://commitweb.herokuapp.com";
          } else {
            // the user isn't logged in to Facebook.
            window.location = "https://commitweb.herokuapp.com";
          }
         });
  }

  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });

  // This function is called when someone finishes with the Login
  // Button.  See the onlogin handler attached to it in the sample
  // code below.
  function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  }



  };
  // END OF ASYNC FB, MAKE CALLS TO FB UP HERE
    // Load the SDK asynchronously
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));



    

  

  // This is called with the results from from FB.getLoginStatus().
  function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    console.log(response.status);
    console.log(response.authResponse.accessToken);

    if (response.status === 'connected') {
      	// Logged into your app and Facebook.
      	var uid = response.authResponse.userID;
		    var shortToken = response.authResponse.accessToken;
        var request = new XMLHttpRequest();
        request.open("GET", "https://commitweb.herokuapp.com/commit/"+shortToken, false);
        //request.open("GET","https://opendatabeta.herokuapp.com/api", false);
        request.send();
        console.log(request.status);
        console.log(request.statusText);
        console.log(request.response);
        console.log(request.response.access_token);
        longToken = request.response.access_token;
        tmpresponse = request.response;


    } else {
      // The person is not logged into your app or we are unable to tell.
      document.getElementById('status').innerHTML = 'Please log ' +
        'into this app.';
    }
  }

  
  // init used to go here


