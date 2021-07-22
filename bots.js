const VkBot = require('node-vk-bot-api');
const {Client} = require('pg')
process.env.NODE_TLS_REJECT_UNAUTHORIZED='0'
const urlDatabase = 'postgres://xbwoosfturwnmu:4f3f0a25361cac11df1af8a3dfe11469029a422f85e055fa1f6072cb1c4b48c3@ec2-54-73-68-39.eu-west-1.compute.amazonaws.com:5432/d4g1mkv1jennht';
const client = new Client({
	user: 'xbwoosfturwnmu',
	host: 'ec2-54-73-68-39.eu-west-1.compute.amazonaws.com',
	password: '4f3f0a25361cac11df1af8a3dfe11469029a422f85e055fa1f6072cb1c4b48c3',
	database: 'd4g1mkv1jennht',
	port: '5432',
	ssl: true
})
function selectHomework(date, dayMonth, dayYear=new Date().getYear())
{
	try{
	console.log('select homework')
		return client.query(
			'SELECT lesson, homework FROM homeworktable WHERE dayNum=$1 and dayMonth=$2 and dayYear=$3',
			[date, dayMonth, dayYear],  
			(err,res) => {
				if (err){
				console.log(err)
				return '@mezhendosina, чето сломамломсь'
				}
				let i = 'Домаха на ${res.rows[0].day} \n\n' + res.rows.map(function(item){ return item.lesson + ": " + item.homework}).join("\n");
				return i
			})
	}
	catch(err){
		console.log(err)
	}
}
function sendHomework(day=null, month=null) {
	var date = new Date()
	console.log('send homework')
	if (day != null & month != null){
		try{
			return selectHomework(day, month, 2021)
		}
		catch(err){
			console.log(err)
		}
	}
	switch (date.getDay()) {
		case 6:
			let homework1 = selectHomework(date.getDate(), date.getMonth())
			date.setDate(date.getDate()+2);
			let homework2 = selectHomework(date.getDate(), date.getMonth())
			return homework1 + homework2
			break
		default:
			date.setDate(date.getDate() + 1)
			return selectHomework()
	}
	
}
async function BotVk() {
	try{
		await client.connect()

		const bot = new VkBot('a9fc970aabe2a7043e253216e66889c81c9f79bc597f15c1c629cfc5ea96760d3c962645be7327b86f6a3');

		/*bot.command('/', (ctx) => {
			console.log('Someone send /. I send /')
			ctx.reply('/');
		});*/

		bot.command('Че задали', (ctx) => {
			console.log('Someone send request for homework')
			var date = new Date();
			ctx.reply(sendHomework(27,4))
			/*
			switch (date.getMonth()) {
				case 6:
				case 7:
				case 8:
					console.log('Someone are stupid')
					ctx.reply('Ты чё, какая домаха? Сейчас лето же - иди отдыхай')
					break
				default:
					ctx.reply(sendHomework())
					break
				}*/
			});
		/*
		bot.command('/CheZadali1',(ctx) =>{
			sendHomework(2,27,4).then(
				ctx.reply());
			console.log('Someone send /CheZadali1')
			ctx.reply()
		});*/
		await bot.startPolling((err) => {
				if (err) {
				console.error(err);
				}
			});
	}
	catch(error){
		console.log(error)
	}
}

BotVk();
module.exports = BotVk;
