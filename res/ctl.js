// --- --- ---
// Controller Main
// --- --- ---

var c = {};
var x = new XMLHttpRequest();
var s = 400;

// handle
var angle = 0;
var h = nipplejs.create({
    zone: document.getElementById('handle'),
    mode: 'dynamic',
    color: '#069',
    lockY: true,
    size: s
});
h.on("move start end",function(event,data){
    if(event.type == "start"){
    }
    if(event.type == "move"){
        angle = Math.round(Math.sin(data.angle.radian)*data.distance/s*2*44*10)/10;
    }
    if(event.type == "end"){
        angle = 0
    }
});
// throttle
var pw = 0;
var t = nipplejs.create({
    zone: document.getElementById('throttle'),
    mode: 'dynamic',
    color: '#111',
    lockX: true,
    size: s
});
t.on("move start end",function(event,data){
    if(event.type == "start"){
    }
    if(event.type == "move"){
        pw = Math.round(Math.cos(data.angle.radian)*data.distance/s*2*20*10)/10;
    }
    if(event.type == "end"){
        pw = 0
    }
});

setInterval(function(){
    if(c.angle != angle || c.pw != pw){
        console.log(angle+'_'+pw);
        x.open('GET','/state/'+angle+'_'+pw);
        x.send(null);
    }
    c.angle = angle;
    c.pw = pw;
},100);



