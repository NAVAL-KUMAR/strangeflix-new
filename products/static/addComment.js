jQuery(document).ready(function () {
  $("#form_comment").submit(function (event) {
    event.preventDefault();
    $.ajax({
      type: "POST",
      url: "/comment",
      data: {
         comment_text: $('#comment').val(),
            video_id : $('#video_id').val(),
            csrfmiddlewaretoken : $('input[name = csrfmiddlewaretoken]').val()
      },
      success: function (response) {
      console.log(response);
        $('#commment_list').empty();
        for(var key in response.comments){
            var temp = "<tr><td>"+response.comments[key].user+"</td>"+"<td>"+response.comments[key].text+"</td>"+"<td>"+response.comments[key].datetime+"</td></tr>";

            $('#commment_list').append(temp);
           // console.log($('#comment_list'));
        }
      }
    });
    return false;
  });
});

 jQuery(document).ready(function () {
  $("#liked").click(function (event) {
    event.preventDefault();
    $.ajax({
      type: "GET",
      url: "/liked",
       data: {
            video_id : $('#video_id').val()
      },
      success: function (response) {
      console.log(response);
        if(response.like == 1){

            document.getElementById('liked').style.color='blue';
            document.getElementById('disliked').style.color='grey';
        }
        else
            document.getElementById('liked').style.color='grey';

         document.getElementById('total_likes').innerHTML =response.total_like+" <i class='fa fa-thumbs-up' style='font-size:20px;color:grey;'> </i>";
         document.getElementById('total_dislikes').innerHTML =response.total_dislike+" <i class='fa fa-thumbs-down' style='font-size:20px;color:grey;'> </i>";
      }
    });
    return false;
  });
});

 jQuery(document).ready(function () {
  $("#disliked").click(function (event) {
    event.preventDefault();
    $.ajax({
      type: "GET",
      url: "/disliked",
      data: {
            video_id : $('#video_id').val()
      },
      success: function (response) {
      console.log(response);
         if(response.dislike == -1){
            document.getElementById('disliked').style.color='red';
            document.getElementById('liked').style.color='grey';
            }
        else
            document.getElementById('disliked').style.color='grey';
         document.getElementById('total_dislikes').innerHTML =response.total_dislike+" <i class='fa fa-thumbs-down' style='font-size:20px;color:grey;'> </i>";
         document.getElementById('total_likes').innerHTML =response.total_like+" <i class='fa fa-thumbs-up' style='font-size:20px;color:grey;'> </i>";
      }
    });
    return false;
  });
});


 jQuery(document).ready(function () {
  $("#favourite").click(function (event) {
    event.preventDefault();
    $.ajax({
      type: "GET",
      url: "/favourite",
      data: {
            video_id : $('#video_id').val()
      },
      success: function (response) {
      console.log(response);
            if(response.fav){
            alert("Video Added to Favourite");
            document.getElementById('favourite').style.color='red';
            }
            else
            document.getElementById('favourite').style.color='grey';
       }
    });
    return false;
  });
});

var theVideo = document.getElementById("my_video");

  document.onkeydown = function(event) {
        console.log(event.keyCode);
      switch (event.keyCode) {
         case 37:
              event.preventDefault();

              vid_currentTime = theVideo.currentTime;
              theVideo.currentTime = vid_currentTime - 10;
            break;

         case 39:
              event.preventDefault();

              vid_currentTime = theVideo.currentTime;
              theVideo.currentTime = vid_currentTime + 10;
            break;
         

      }
  };
