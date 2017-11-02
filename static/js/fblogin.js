var finished_rendering = function() {
console.log("finished rendering plugins");
var spinner = document.getElementById("spinner");
spinner.removeAttribute("style");
spinner.removeChild(spinner.childNodes[0]);
}
// local
// 196208740925120
// remote
// 2024489881171070

window.fbAsyncInit = function() {
  FB.init({
    appId      : '196208740925120',
    cookie     : true,  // enable cookies to allow the server to access 
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.8' // use graph api version 2.8
  });

  FB.Event.subscribe('xfbml.render', finished_rendering);

  // FB.getLoginStatus(function(response) {
  //   statusChangeCallback(response);
  // });

  };

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
    console.log('statusChangeCallback2');
    console.log(response);

    if (response.status === 'connected') {
      // Logged into your app and Facebook.

      testAPI();


      // REDIRECT
      window.location = "../../fancycommitlanding";

    } else {
      // The person is not logged into your app or we are unable to tell.
      //document.getElementById('status').innerHTML = 'Please log ' + 'into this app.';
      window.location = "../../fancycommitlanding";
    }
  }

  // This function is called when someone finishes with the Login
  // Button.  See the onlogin handler attached to it in the sample
  // code below.
  function checkLoginState() {

    FB.getLoginStatus(function(response) {
      console.log('getLoginStatus');
      console.log(response);
      statusChangeCallback(response);
    });

  }
  // Here we run a very simple test of the Graph API after login is
  // successful.  See statusChangeCallback() for when this call is made.
  function testAPI() {
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      console.log('Successful login for: ' + response.name);
    });

  }

