const user_id = JSON.parse(document.getElementById('user_id').textContent);

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
            var temp = '<div class="card my-2"> <div class="card-header"> <div class="float-left">'+response.comments[key].name+'</div> <div class="float-right">';
                    if(user_id == response.comments[key].user_id){

                     temp = temp + '<button id = "e'+response.comments[key].id+'" class="btn btn-primary mx-1" onclick="openForm(this)"><strong><i class="fa fa-pencil"  style="font-size:20px;" aria-hidden="true"></i></strong></button>';
                    temp = temp + '<button id = "d'+response.comments[key].id+'"class="btn btn-danger mx-1" onclick="delete_comment(this)"><strong><i class="fa fa-trash" style="font-size:20px;" aria-hidden="true"></i></strong></button>';

                    }

                    temp = temp + '<button id="f'+response.comments[key].id+'"class="btn btn-success" onclick="openForm_flag(this)"><strong><i class="fa fa-flag" style="font-size:20px;" aria-hidden="true"></i></strong></button>';
                     temp = temp + '</div> </div> <div class="card-body">  <blockquote class="blockquote mb-0"> <p>'+response.comments[key].text+'</p> <footer class="blockquote-footer">'+response.comments[key].date_prety+'</footer>  </blockquote> </div> </div>';


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

//  document.onkeydown = function(event) {
//        console.log(event.keyCode);
//      switch (event.keyCode) {
//         case 37:
//              event.preventDefault();
//
//              vid_currentTime = theVideo.currentTime;
//              theVideo.currentTime = vid_currentTime - 10;
//            break;
//
//         case 39:
//              event.preventDefault();
//
//              vid_currentTime = theVideo.currentTime;
//              theVideo.currentTime = vid_currentTime + 10;
//            break;
//         case 32:
//            event.preventDefault();
//            if(vid.paused){
//                vid.play();
//                document.getElementById('playpausebtn').className='fa fa-play';
//            }else{
//                vid.pause();
//                document.getElementById('playpausebtn').className='fa fa-pause';
//            }
//            break;
//
//      }
//  };

  function delete_comment(id){
            $.ajax({
              type: "GET",
              url: "/delete_comment",
              data: {
                    video_id : $('#video_id').val(),
                    comment_id : parseInt(id.id.substring(1))
              },
              success: function (response) {
                console.log(response);
                $('#commment_list').empty();
                for(var key in response.comments){
                    var temp = '<div class="card my-2"> <div class="card-header"> <div class="float-left">'+response.comments[key].name+'</div> <div class="float-right">';
                    if(user_id == response.comments[key].user_id){

                     temp = temp + '<button id = "e'+response.comments[key].id+'" class="btn btn-primary mx-1" onclick="openForm(this)"><strong><i class="fa fa-pencil"  style="font-size:20px;" aria-hidden="true"></i></strong></button>';
                    temp = temp + '<button id = "d'+response.comments[key].id+'"class="btn btn-danger mx-1" onclick="delete_comment(this)"><strong><i class="fa fa-trash" style="font-size:20px;" aria-hidden="true"></i></strong></button>';

                    }
                    temp = temp + '<button id="f'+response.comments[key].id+'"class="btn btn-success" onclick="openForm_flag(this)"><strong><i class="fa fa-flag" style="font-size:20px;" aria-hidden="true"></i></strong></button>';


                    temp = temp + '</div> </div> <div class="card-body">  <blockquote class="blockquote mb-0"> <p>'+response.comments[key].text+'</p> <footer class="blockquote-footer">'+response.comments[key].date_prety+'</footer>  </blockquote> </div> </div>';

                    $('#commment_list').append(temp);
                   // console.log($('#comment_list'));
                }
            }
            });
  }


 function openForm(id) {
        document.getElementById("popupForm").style.display = "block";


        $(document).ready(function () {
            $("#edit").click(function () {
                var txt = $("#editcomment").val();

                $.ajax({
              type: "GET",
              url: "/edit_comment",
              data: {
                    video_id : $('#video_id').val(),
                    comment_id : parseInt(id.id.substring(1)),
                    text : txt
              },
              success: function (response) {
                console.log(response);
                $('#commment_list').empty();
                for(var key in response.comments){
                   var temp = '<div class="card my-2"> <div class="card-header"> <div class="float-left">'+response.comments[key].name+'</div> <div class="float-right">';
                    if(user_id == response.comments[key].user_id){

                     temp = temp + '<button id = "e'+response.comments[key].id+'" class="btn btn-primary mx-1" onclick="openForm(this)"><strong><i class="fa fa-pencil"  style="font-size:20px;" aria-hidden="true"></i></strong></button>';
                    temp = temp + '<button id = "d'+response.comments[key].id+'"class="btn btn-danger mx-1" onclick="delete_comment(this)"><strong><i class="fa fa-trash" style="font-size:20px;" aria-hidden="true"></i></strong></button>';

                    }

                    temp = temp + '<button id="f'+response.comments[key].id+'"class="btn btn-success" onclick="openForm_flag(this)"><strong><i class="fa fa-flag" style="font-size:20px;" aria-hidden="true"></i></strong></button>';


                    temp = temp + '</div> </div> <div class="card-body">  <blockquote class="blockquote mb-0"> <p>'+response.comments[key].text+'</p> <footer class="blockquote-footer">'+response.comments[key].date_prety+'</footer>  </blockquote> </div> </div>';


                    $('#commment_list').append(temp);
                   // console.log($('#comment_list'));
                }
                document.getElementById("popupForm").style.display = "none";
            }
            });
            return false;
            });
        });

  }

    function closeForm() {
    document.getElementById("popupForm").style.display = "none";
    }


    function openForm_flag(id) {
        document.getElementById("popupForm_flag").style.display = "block";


        $(document).ready(function () {
            $("#send").click(function () {
                var txt = $("#send_reason").val();

                $.ajax({
              type: "GET",
              url: "/add_comment_flag",
              data: {
                    video_id : $('#video_id').val(),
                    comment_id : parseInt(id.id.substring(1)),
                    text : txt
              },
              success: function (response) {
                alert("comment reported sucessfully");
                document.getElementById("popupForm_flag").style.display = "none";
            }
            });
            return false;
            });
        });

  }

function closeForm_flag() {
    document.getElementById("popupForm_flag").style.display = "none";
    }

  function closeForm_flag_btn() {
    document.getElementById("popupForm_v_flag").style.display = "none";
    }
    function openForm_flag_video(id) {
        document.getElementById("popupForm_v_flag").style.display = "block";


        $(document).ready(function () {
            $("#send_flag").click(function () {
                var txt = $("#reason_to_flag").val();

                $.ajax({
              type: "GET",
              url: "/add_video_flag",
              data: {
                    video_id : $('#video_id').val(),
                    text : txt
              },
              success: function (response) {
                alert("video reported sucessfully");

                document.getElementById("popupForm_v_flag").style.display = "none";
            }
            });
            return false;
            });
        });

  }

    function ignore_v(id){

            $.ajax({

              type: "GET",
              url: "/ignore_v",
              data: {

                    notification_v_id : parseInt(id.id)
              },
              success: function (response) {

                $('#notf').empty();
                var temp = '';
                for(var key in response.flg){
            temp = temp + ' <div ';
if (response.flg[key].user_response)
    temp = temp + 'style = "background-color: rgba(18,90,87,0.5);margin-left: 5px;margin-right: 5px; padding: 5px 8px;"';
else
    temp = temp + 'style = "background-color: rgba(90,255,101,0.5);margin-left: 5px;margin-right: 5px;padding: 5px 8px;"';
temp = temp + '><P>'+response.flg[key].name+' <button id = "'+response.flg[key].id+'" onclick = "ignore_goto_video(this)" style = "margin-left: 5px;" > Go To Video </button ><button id = "'+response.flg[key].id+'" onclick = "ignore_v(this)" style = "margin-left: 5px;" > Ignore </button >';
 if(typeof response.flg[key].comment!= 'undefined')
  temp = temp + '<button id="d'+response.flg[key].id+'"onclick="delete_comm(this)"  style="cursor: pointer;" >delete comment</button>';

temp = temp + '<span style = "float: right;"> '+response.flg[key].date+' </span > </P > <h4 > '+response.flg[key].reason+' </h4 > </div > <div style="background-color: white;height: 10px;"></div>';



        }
        document.getElementById('notf').innerHTML = temp;



            }
            });
  }

  function ignore_goto_video(id){
    $.ajax({
       type: "GET",
              url: "/ignore_goto_video",
              data: {

                    notification_v_id : parseInt(id.id.substring(1))
              },
              success: function(response){
                 console.log(response.id);
                 window.location.href = response.redirect;
              }
    });
  }


 jQuery(document).ready(function () {
    setInterval(function()
    {
    $.ajax({
      type: "GET",
      url: "/save_video_time",
       data: {
            video_id : $('#video_id').val(),
            time : document.getElementById('my_video').currentTime,
            end : document.getElementById('my_video').duration
      },
      success: function (response) {
        console.log(response);
      }
    });
    },1000);
});

function delete_comm(id){
    $.ajax({
       type: "GET",
              url: "/delete_comm",
              data: {

                    notf_id : parseInt(id.id.substring(1))

              },
              success: function(response){

                 alert("comment deleted sucessfully");
              }
    });
  }


