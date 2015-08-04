var time = Date.now();
var timep = time;
var system = require('system');
var page = require('webpage').create();
var fs = require('fs');

function logTime(label, fromTime){
	var s = "Time";
	if (label) s = label;
	var t = Date.now();
	var o = timep.time || timep;
	var logmsg ="@"+((t - time)/1000)+"s" + "\t+"+((t - o)/1000)+"s\t" + s;
	if (fromTime !== undefined){
		if (fromTime === fromTime-0) fromTime = {time:fromTime};
		logmsg += " (+"+((t - fromTime.time)/1000)+"s"+((fromTime.label)?" from: "+fromTime.label:"")+")";
	}
	console.log(logmsg); 
	timep={label:label,time:t};
	return timep;
}

var p = "";
var type = ""; 
var folder = "";

if (system.args.length > 1)
	p = system.args[1];

if (system.args.length > 2)
	type = system.args[2];
	
if (system.args.length > 3)
	folder = system.args[3];
	

global.type = type;

logTime("system.args[1]="+system.args[1]);
logTime("system.args[2]="+system.args[2]);
logTime("system.args[3]="+system.args[3]);

var arrURL = p.split("/");

var idURL = arrURL[arrURL.length-1]; 
logTime("idURL="+idURL);

page.onInitialized = function() {
  page.evaluate(function() {
    //Disable d3's transitions API
	//https://github.com/mbostock/d3/issues/1789
	window.flushAnimationFrames = function() {
	  var now = Date.now;
	  Date.now = function() { return Infinity; };
	  d3.timer.flush();
	  Date.now = now;
	};
  });
};

logTime("Loading page: "+p);

page.open(p, function(status) {

	logTime("Page Loaded");
	logTime("type="+type);

	//fs.write('output/static_'+idURL+'.html', page.content, 'w');
	//logTime("Static html created");
	
	page.viewportSize = {
		width: 1200,
		height: 655
	};
	
	//page.onConsoleMessage = function (msg) { logTime(msg); };
	
	//console.log(JSON.stringify(page.viewportSize, null, 4));
	//console.log(JSON.stringify(page.clipRect, null, 4));

	var clipRect = page.evaluate( function(type) {  
		try { 
	
			flushAnimationFrames(); // Render visualisation's final state

			flushAnimationFrames(); // Render visualisation's final state

			for (i = 0; i < 100000; i++) { 
    
				for (ii = 0; ii < 10000; ii++) { 
	    
				}

			}
						
			//var rect = document.querySelector(".container_graph").getBoundingClientRect(); // Measure svg container 
			//var svg = document.querySelector(".container_graph > svg"); // svg's container has display:block covering the more width than the svg. Can be fixed with display:inline-block.
			

				var rect = document.querySelector(".pc_chart").getBoundingClientRect(); // Measure svg container 
				var svg = document.querySelector(".pc_chart"); // svg's container has display:block covering the more width than the svg. Can be fixed with display:inline-block.
				
			
				if (rect.top==0)
				{				
					//var rect = document.querySelector(".datamap").getBoundingClientRect(); // Measure svg container 
					//var svg = document.querySelector(".datamap"); // svg's container has display:block covering the more width than the svg. Can be fixed with display:inline-block.				
				
				
					var rect = document.querySelector(".leaflet-zoom-animated").getBoundingClientRect(); // Measure svg container 
					var svg = document.querySelector(".leaflet-zoom-animated"); // svg's container has display:block covering the more width than the svg. Can be fixed with display:inline-block.
					
				
				}

			
				return {
					top: rect.top,
					left: rect.left,
					//width: svg.clientWidth,
					width: rect.width,
					height: rect.height
				};
			
							
		} catch (e) {
			console.log("Can't locate a graph container or svg");
			//logTime("Can't locate a graph container or svg");
			
			return {
					top: 0,
					left: 0,
					//width: svg.clientWidth,
					width: 0,
					height: 0
				};
			
		}
	}, type);
	
	logTime("clipRect.top:"+clipRect.top);



	var ft = logTime("Visualisation measured");
	
	var oldClip = page.clipRect;
	page.clipRect = clipRect;
	
	//page.render('/home/miquel/PolicyCompass/policycompass/pc-services-miquel/policycompass-services/apps/visualizationsmanager/phantomCapture/output/'+type+'_'+idURL+'.png');
	
	page.render(folder+type+'_'+idURL+'.png');
	
	logTime("Visualisation captured", ft);
	

	page.close();
	setTimeout(phantom.exit, 0);
	

});


