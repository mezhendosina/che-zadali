
var spawn = require("child_process").spawn;
var vkBot = require('./bots')
var login = require('./login')
async function firstStep(){
	var process = spawn('python',[/*Path to py script*/], homework);
	const homework = login().then(
		process.stdout.on('data', function(data){
    		console.log('homework parsed')
		})
	);
}

setTimeout(function() {
	firstStep()
}, 1000);
setTimeout(function(){
	vkBot()
}, 0);