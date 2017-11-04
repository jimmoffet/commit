
var uid = '';
var shortToken = '';
var tmpresponse;
var globalresponse;
var longToken = '';
var friends;
var carleypicurl;
var dict;

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
        request.open("GET", "/commit/"+shortToken, false);
        request.send();
        console.log(request.status);
        console.log(request.statusText);
        console.log(request.response);
        //console.log(request.response.access_token);
        longToken = request.response;

        tagFriendsCall = "/"+ uid +"/taggable_friends";
        
        
        /* make the API call */
        FB.api(
            tagFriendsCall,
            function (response) {
              if (response && !response.error) {
                friends = response;
                console.log('got friends')
              } else {
                console.log('something has gone horribly wrong getting taggable friends')
              }
            }
        );

        //longToken = request.response;
        longToken = longToken.replace(/(\r\n|\n|\r)/gm,"");
        longToken = JSON.parse(longToken).access_token;
        //carleypicurl = friends.data[14].picture.data.url;
        dict = JSON.stringify({
              "uid":uid,
              "longToken":longToken,
              "taggable_friends":friends,
              "foo":"foo"
            });

        $.ajax({
            url: '/api',
            data: JSON.stringify({
              "uid":uid,
              "longToken":longToken,
              "taggable_friends":friends,
              "foo":"foo"
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
      window.location = "/";
      FB.logout(function(response) {
        // user is now logged out
        console.log(response);
        window.location = "/";
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
      window.location = "/fancycommitlanding2";
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
      location.href = "/fancycommitlandingFINAL";
      console.log('sent to fancycommitlanding2');
    }

  function resetCursor(txtElement) { 
    if (txtElement.setSelectionRange) { 
        txtElement.focus(); 
        txtElement.setSelectionRange(0, 0); 
    } else if (txtElement.createTextRange) { 
        var range = txtElement.createTextRange();  
        range.moveStart('character', 0); 
        range.select(); 
    } 
}

