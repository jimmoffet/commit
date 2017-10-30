
var uid = '';
var shortToken = '';
var tmpresponse;
var globalresponse;
var longToken = '';
var friends;

const timeStamp = () => {
  let options = {
    month: '2-digit',
    day: '2-digit',
    year: '2-digit',
    hour: '2-digit',
    minute:'2-digit'
  };
  let now = new Date().toLocaleString('en-US', options);
  return now;
};

window.fbAsyncInit = function() {
  FB.init({
    appId      : '2024489881171070',
    cookie     : true,  // enable cookies to allow the server to access 
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.8' // use graph api version 2.8
  });

  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });

  // This function is called when someone finishes with the Login
  // Button.  See the onlogin handler attached to it in the sample
  // code below.
  
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
        request.send();
        console.log(request.status);
        console.log(request.statusText);
        console.log(request.response);
        //console.log(request.response.access_token);
        longToken = request.response;
        tmpresponse = request.response;

        // var request2 = new XMLHttpRequest();
        // request2.open("GET", "https://commitweb.herokuapp.com/writeuser/"+uid, false);
        // request2.send();
        // console.log(request2.status);
        // console.log(request2.statusText);
        // console.log(request2.response);

        tagFriendsCall = "/"+ uid +"/taggable_friends";
        
        /* make the API call */
        FB.api(
            "/1422652447849585/taggable_friends",
            function (response) {
              if (response && !response.error) {
                friends = response;
                console.log('got friends')
              } else {
                console.log('something has gone horribly wrong getting taggable friends')
              }
            }
        );

        longToken = longToken.replace(/(\r\n|\n|\r)/gm,"");
        longToken = JSON.parse(longToken).access_token;

        $.ajax({
            url: 'https://commitweb.herokuapp.com/api',
            data: JSON.stringify({
              "uid":uid,
              "longToken":longToken,
              "timeStamp":timeStamp,
              "taggable_friends":friends
            }),
            dataType: 'json',
            contentType: "application/json",
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });



    } else {
      // The person is not logged into your app or we are unable to tell.
      document.getElementById('status').innerHTML = 'Please log ' +
        'into this app.';
    }
  }

  function checkLoginState() 
    {
      FB.getLoginStatus(function(response) {
        statusChangeCallback(response);
      });
    }

  function logoutFacebook()
    {
      FB.logout(function(response) {
        // user is now logged out
        console.log(response);
        window.location = "https://commitweb.herokuapp.com";
      });
    }

  function sendPositive(e) 
    {
      //e.preventDefault();
      let positive_message = document.getElementById("ghost-input").value;
      var request = new XMLHttpRequest();
      request.open("GET", "/positive/"+positive_message, false);
      request.send();
      console.log(request.status);
      console.log(request.statusText);
      console.log(request.response);
      window.location = "https://commitweb.herokuapp.com/fancycommitlanding2";
      console.log('sent to fancycommitlanding2');
    }

  function sendNegative(e) 
    {
      //e.preventDefault();
      let negative_message = document.getElementById("ghost-input").value;
      var request = new XMLHttpRequest();
      request.open("GET", "/negative/"+negative_message, false);
      request.send();
      console.log(request.status);
      console.log(request.statusText);
      console.log(request.response);
      location.href = "https://commitweb.herokuapp.com/fancycommitlandingFINAL";
      console.log('sent to fancycommitlanding2');
    }

