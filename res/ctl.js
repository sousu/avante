// --- --- ---
// Controller Main
// --- --- ---
(function(){
    // common
    var angle = 0;
    var pw = 0;
    
    // web-base joystick (nipplejs)
    var s = 330;  // stick size
    var h = nipplejs.create({
        zone: document.getElementById('handle'),
        mode: 'dynamic',
        color: '#069',
        lockY: true,
        size: s
    });
    h.on("move start end",function(event,data){
        if(event.type == "start"){}
        if(event.type == "move"){
            angle = Math.round(Math.sin(data.angle.radian)*data.distance/s*2*-44);
        }
        if(event.type == "end"){
            angle = 0
        }
    });
    var t = nipplejs.create({
        zone: document.getElementById('throttle'),
        mode: 'dynamic',
        color: '#111',
        lockX: true,
        size: s
    });
    t.on("move start end",function(event,data){
        if(event.type == "start"){}
        if(event.type == "move"){
            pw = Math.round(Math.cos(data.angle.radian)*data.distance/s*2*35);
        }
        if(event.type == "end"){
            pw = 0
        }
    });

    // gamepad API
    var gi = 100; // interval
    var gc = null; 
    if(navigator.getGamepads){
        addEventListener("gamepadconnected",function(){
            console.log("gamepad connected");
            gc = setInterval(function(){
                var gp = navigator.getGamepads()[0];
                if(!gp) return;
                angle = Math.round(gp.axes[0]*44); // left X
                pw = Math.round(gp.axes[3]*-35);   // right Y
            },gi);
        });
        addEventListener("gamepaddisconnected",function(){
            console.log("gamepad disconnected");
            window.clearInterval(gc);
        });
    }

    // main 
    var i = 100;  // request interval
    var da = 3;   // effective diff angel
    var dp = 3;   // effective diff power
    var x = new XMLHttpRequest();
    var c = {};
    setInterval(function(){
        if(Math.abs(c.angle-angle) < da && Math.abs(c.pw-pw) < dp) return;
        console.log(angle+'_'+pw);
        x.open('GET','/state/'+angle+'_'+pw);
        x.send(null);
        c.angle = angle;
        c.pw = pw;
    },i);
}());


