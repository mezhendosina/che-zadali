/// TO-DO: import js files 
var spawn = require("child_process").spawn;
var vkBot = require('./bots')
var login = require('./login')
async function firstStep(){
	var process = spawn('python',[/*Path to py script*/], homework);
	const homework = login().then(
		result => process.stdout.on('data', function(data){
    		console.log('homework parsed')
		})
		error => console.log('error')
	);
}

setTimeout(function() {
	firstStep()
}, 1000);
setTimeout(function(){
	vkBot()
}, 0);
/* "dependencies": {
    "puppeteer": "^10.1.0",
    "node-vk-bot-api": "^3.5.0",
    "@notionhq/client": "^0.2.2"
  },
  */