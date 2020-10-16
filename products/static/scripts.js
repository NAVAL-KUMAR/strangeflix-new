var vid, playbtn ,volumeslider, mutebtn, curtimetext, durtimetext, seekslider , videoPlayerBox , fullScreenBtn , backward10 , forward10;

function initializeplayer(){
    event.preventDefault();
    vid = document.getElementById('my_video');
    playbtn = document.getElementById('playpausebtn');
    videoPlayerBox = document.getElementById('video_player_box');
    fullScreenBtn = document.getElementById('fullscreenbtn');
    backward10 = document.getElementById('backward10');
    forward10 = document.getElementById('forward10');
    seekslider = document.getElementById('seekslider');
    curtimetext = document.getElementById('curtimetext');
    durtimetext = document.getElementById('durtimetext');
    mutebtn = document.getElementById('mutebtn');
    volumeslider = document.getElementById('volumeslider');

    playbtn.addEventListener("click",playPause,false);
    forward10.addEventListener("click",forward10sec,false);
    backward10.addEventListener("click",backward10sec,false);
    fullScreenBtn.addEventListener("click",fullScreen,false);
    seekslider.addEventListener("change",vidSeek,false);
    vid.addEventListener("timeupdate",seektimeupdate,false);
    mutebtn.addEventListener("click",vidmute,false);
    volumeslider.addEventListener("change",setvolume,false);
    videoPlayerBox.addEventListener("mouseover",makevisible,false);
}

window.onload = initializeplayer;

function playPause(){
    if(vid.paused){
        vid.play();
        playbtn.className='fa fa-play';
    }else{
        vid.pause();
        playbtn.className='fa fa-pause';
    }
}

function forward10sec(){
    vid_currentTime = vid.currentTime;
    vid.currentTime = vid_currentTime + 10;
}

function backward10sec(){
    vid_currentTime = vid.currentTime;
    vid.currentTime = vid_currentTime - 10;
}

function fullScreen(){
    if (!document.fullscreenElement) {
        videoPlayerBox.requestFullscreen();
        fullScreenBtn.className="fa fa-arrows-h";
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
            fullScreenBtn.className="fa fa-arrows-alt";
        }
    }

}

function vidSeek(){
    var seekto = vid.duration*(seekslider.value/100);
    vid.currentTime = seekto;
}

function seektimeupdate(){
    var nt = vid.currentTime*(100/vid.duration);
    seekslider.value = nt;
    var curmins = Math.floor(vid.currentTime/60);
    var cursecs = Math.floor(vid.currentTime - curmins*60);
    var durmins = Math.floor(vid.duration/60);
    var dursecs = Math.floor(vid.duration - durmins*60);

    if(cursecs < 10) cursecs = "0"+cursecs;
    if(curmins < 10) curmins = "0"+curmins;
    if(durmins < 10) durmins = "0"+durmins;
    if(dursecs < 10) dursecs = "0"+dursecs;

    curtimetext.innerHTML = curmins+":"+cursecs+"/";
    durtimetext.innerHTML = durmins+":"+dursecs;
}

function vidmute(){
    if(vid.muted){
        vid.muted = false;
        volumeslider.value = 100;
        mutebtn.className="fa fa-volume-up";
    }else{
        vid.muted = true;
        volumeslider.value = 0;
        mutebtn.className="fa fa-volume-off";
    }
}

function setvolume(){
    vid.volume = volumeslider.value/100;
}

function makevisible(){
    document.getElementById("video_control_bar").hide();
}