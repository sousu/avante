// --- --- ---
// Connection Monitor 
// --- --- ---
(function(){
    function loadFile(url,timeout,callback) {
        var args = Array.prototype.slice.call(arguments,3);
        var xhr = new XMLHttpRequest();
        xhr.ontimeout = function () {
            console.error("request for " + url + " timed out");
        };
        xhr.onload = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    callback.apply(xhr,args);
                } else {
                    console.error(xhr.statusText);
                }
            }
        };
        xhr.open("GET",url,true);
        xhr.timeout = timeout;
        xhr.send(null);
    }
    setInterval(function() {
        //var dd = new Date();
        //document.getElementById("conn").innerHTML = dd.toLocaleString();
        loadFile("res/conn",1000,function(){
            document.getElementById("conn").innerHTML = this.responseText;
        });
    }, 2000);
})();

