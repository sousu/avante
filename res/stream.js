
window.onload = function(){
    var s = document.getElementById("stream");
    var u = "http://"+location.hostname+":9999/?action=stream";
    var i = new Image();
    i.onload = function(){
        console.log("streaming exist");
        s.src = u;
    }
    i.src = u;
}

