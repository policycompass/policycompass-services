var path = require('path')
var childProcess = require('child_process')
var phantomjs = require('phantomjs')
var binPath = phantomjs.path
 
var url = process.argv[2];
var type = process.argv[3];
var folder = process.argv[4];

console.log("main");
console.log("url");
console.log(url);
//url = "https://alpha.policycompass.eu/app/#/visualizations/2";
//url = "https://alpha.policycompass.eu/app/#/visualizations/graph/2";
console.log("type");
console.log(type);
console.log("folder");
console.log(folder);

var childArgs = [
  path.join(__dirname, '/library/capture.js')
];

if (url!=null)
{
	childArgs.push(url, type, folder);
}


childProcess.execFile(binPath, childArgs, function(err, stdout, stderr) {

	console.log("err");
	console.log(err);
	
	console.log("stdout");	
	console.log(stdout);

	console.log("stderr");	
	console.log(stderr);
		
})
