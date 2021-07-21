
var spawn = require("child_process").spawn;
var vkBot = require('./bots')
var login = require('./login')
async function firstStep(){
	const homework = await login()
	var process = spawn('python',['./extractHomewrokFromHTML.py'], homework);
	process.stdout.on('data', function(data){
    		console.log('homework parsed')
		})
}
async function start(){
setTimeout(function() {
	firstStep()
}, 1000);
await setTimeout(function(){
	vkBot()
}, 0);
}
start().then(
Error => console.log('Error')
)
