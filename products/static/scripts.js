var vid, vc , playbtn ,volumeslider, mutebtn, curtimetext, durtimetext, seekslider , videoPlayerBox , fullScreenBtn , backward10 , forward10 , playback2 ,playback1_5,playback1,playback0_5,playback0_25;

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
    playback2 = document.getElementById('playback2.0');
    playback1_5 = document.getElementById('playback1.5');
    playback1 = document.getElementById('playback1.0');
    playback0_5 = document.getElementById('playback0.5');
    playback0_25 = document.getElementById('playback0.25');

    playbtn.addEventListener("click",playPause,false);
    forward10.addEventListener("click",forward10sec,false);
    backward10.addEventListener("click",backward10sec,false);
    fullScreenBtn.addEventListener("click",fullScreen,false);
    playback2.addEventListener("click",playback2speed,false);
    playback1_5.addEventListener("click",playback1_5speed,false);
    playback1.addEventListener("click",playback1speed,false);
    playback0_5.addEventListener("click",playback0_5speed,false);
    playback0_25.addEventListener("click",playback0_25speed,false);
    vid.addEventListener("click",videocontrol,false);
    seekslider.addEventListener("change",vidSeek,false);

    vid.addEventListener("timeupdate",seektimeupdate,false);
    mutebtn.addEventListener("click",vidmute,false);
    volumeslider.addEventListener("change",setvolume,false);
}

window.onload = initializeplayer;

function playPause(){
    if(vid.paused){
        vid.play();
        playbtn.className='fa fa-pause';
    }else{
        console.log(vid);
        vid.pause();
        playbtn.className='fa fa-play';
    }
}

function videocontrol(){
    if(vid.paused){
        vid.play();
        playbtn.className='fa fa-pause';
    }else{
        console.log(vid);
        vid.pause();
        playbtn.className='fa fa-play';
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

    curtimetext.innerHTML = curmins+":"+cursecs+" ";
    durtimetext.innerHTML = " "+ durmins+":"+dursecs;
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


function playback2speed(){
    vid.playbackRate = 2.0;
}

function playback1_5speed(){
    vid.playbackRate = 1.5;
}

function playback1speed(){
    vid.playbackRate = 1.0;
}

function playback0_5speed(){
    vid.playbackRate = 0.5;
}

function playback0_25speed(){
    vid.playbackRate = 0.25;
}


