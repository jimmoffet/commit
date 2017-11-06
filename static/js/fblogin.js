// var finished_rendering = function() {
// console.log("finished rendering plugins");
// var spinner = document.getElementById("spinner");
// spinner.removeAttribute("style");
// spinner.removeChild(spinner.childNodes[0]);
// }
// local
// 196208740925120
// remote
// 2024489881171070

window.fbAsyncInit = function() {
  FB.init({
    appId      : '2024489881171070',
    cookie     : true,  // enable cookies to allow the server to access
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.8' // use graph api version 2.8
  });

  // FB.Event.subscribe('xfbml.render', finished_rendering);

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
    console.log('running statusChangeCallback');
    console.log(response);

    if (response.status === 'connected') {
      // Logged into your app and Facebook.

      testAPI();


      // REDIRECT
      //window.location = "../../fancycommitevent";



      return [name,longToken,email]

    } else {
      // The person is not logged into your app or we are unable to tell.
      //document.getElementById('status').innerHTML = 'Please log ' + 'into this app.';
      //window.location = "../../fancycommitevent";
      console.log('not connected!');
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



function fbLogin(ref){

    console.log('ref at beginning');
    console.log(ref);
    var name = '';
    var email = '';
    var phone = '';
    var fbId = '';
    var twId = '';
    var fbToken = '';
    var twToken = '';
    var referringUser = ref;
    var uid = '';

    FB.login(function(response) {
          if (response.authResponse) {

             console.log('Welcome!  Fetching your information.... ');
             console.log(response.authResponse);
             console.log('access token is ');
             console.log(response.authResponse.accessToken);
             fbToken = response.authResponse.accessToken;
             fbId = response.authResponse.userID;


             FB.api('/'+fbId+"?fields=name,email", function(response) {

               console.log('Good to see you, ' + response.name + '.');
               console.log(response);
               name = response.name;
               email = response.email;

               console.log('begin');
               console.log(name);
               console.log(email);
               console.log(fbId);
               console.log(fbToken);
               console.log('end');

                $.ajax({
                  url: '/createuser',
                  data: JSON.stringify({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "fbId": fbId,
                    "twId": twId,
                    "fbToken": fbToken,
                    "twToken": twToken,
                    "referringUser": referringUser
                  }),
                  dataType: 'json',
                  contentType: "application/json",
                  type: 'POST',
                  success: function(response) {
                    console.log(response);
                    uid = response;
                    emailUser();
                  },
                  error: function(error) {
                    console.log(error);
                    alert('Failed to create user. Notify Team COMM!T at teamcommitapp@gmail.com');
                  }
                });


              });

             function emailUser(){  
              function emailUser(userId) {
                $.ajax({
                  url: '/mail',
                  data: JSON.stringify({
                    "user": uid
                  }),
                  dataType: 'json',
                  contentType: "application/json",
                  type: 'POST',
                  success: function(response) {
                    console.log(response);
                    window.location= '/commit/'+ref+"A"+uid;
                  },
                  error: function(error) {
                    console.log(error);
                    window.location= '/commit/'+ref+"A"+uid;
                  }
                });


              
             }
              


          } else {
           console.log('User cancelled login or did not fully authorize.');
           console.log('ref at end');
           console.log(ref);
          }
    }, {scope: 'public_profile,email'});

  console.log('ref at end');
  console.log(ref);

}
