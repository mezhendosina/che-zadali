const VkBot = require('node-vk-bot-api');
const {Client} = require('pg')
process.env.NODE_TLS_REJECT_UNAUTHORIZED='0'

const client = new Client({
	connectionString: process.env.DATABASE_URL,
  	ssl: {
    	rejectUnauthorized: false
  }})
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

		const bot = new VkBot(process.env.VK_API_TOKEN);

		/*bot.command('/', (ctx) => {
			console.log('Someone send /. I send /')
			ctx.reply('/');
		});*/

		bot.command('Че задали', (ctx) => {
			console.log('Someone send request for homework')
			var date = new Date();
			ctx.reply(sendHomework(27,4))
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
				}
			});
		
		bot.command('/CheZadali1',(ctx) =>{
			console.log('Someone send /CheZadali1')
			ctx.reply(sendHomework(27,4))
		});
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
