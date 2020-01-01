// --- ---
// Controller Main
// --- ---

var angle = 0
var cur = 0
var s = 300
var xhr = new XMLHttpRequest();
var n = nipplejs.create({
    mode: 'dynamic',
    position: {left: '50%', top: '50%'},
    color: '#069',
    size: s
});

setInterval(function(){
    if(cur != angle){
        console.log(angle);
        xhr.open('GET','/angle/'+angle);
        xhr.send(null);
    }
    cur = angle;
},100); //resolution

n.on("move start end",function(event,data){
    if(event.type == "start"){
    }
    if(event.type == "move"){
        angle = Math.round(Math.cos(data.angle.radian)*data.distance/s*2*44*10)/10;
    }
    if(event.type == "end"){
        angle = 0
    }
});


