const VkBot = require('node-vk-bot-api');
const {Client} = require('pg')

const client = new Client({
			user: 'xbwoosfturwnmu',
			host: 'ec2-54-73-68-39.eu-west-1.compute.amazonaws.com',
			database: 'd4g1mkv1jennht',
			password: '4f3f0a25361cac11df1af8a3dfe11469029a422f85e055fa1f6072cb1c4b48c3',
			port: '5432'
	})

async function sendHomework() {
	var date = new Date()
	async function selectHomework(day=date.getDay()+1, date=date.getDate()+1){
		return await client.query("SELECT day, lesson, homework WHERE dayName='$1' and dayNum='$2' and dayMonth='$3' and dayYear='$4'", [day, date, date.getMonth(), date.getYear()], (err,res) => {
				if (err){
				console.log(err)
				return '@mezhendosina, чето сломамломсь, отправил тебе  ̶̶̶х̶у̶й̶ логи за щеку :)'
				}
				let i = 'Домаха на ${date} \n\n' + res.rows.map(function(item){ return item.lesson + ": " + item.homework}).join("\n");
				return i
	})
	switch (date.getDay()) {
		case 6:
			let homework1 = selectHomework(6, date.getDate())
			let homework2 = selectHomework(1, date.getDate()+2)
			return homework1 + homework2
		default:
			return selectHomework()
			}
	}
}
async function BotVk() {
		await client.connect()

		const bot = new VkBot('a9fc970aabe2a7043e253216e66889c81c9f79bc597f15c1c629cfc5ea96760d3c962645be7327b86f6a3');

		bot.command('/', (ctx) => {
			ctx.reply('/');
		});

		bot.command('Че задали', (ctx) => {
			var date = new Date();
			switch (date.getMonth()) {
				case 6:
				case 7:
				case 8:
					ctx.reply('Ты чё, какая домаха? Сейчас лето же - иди отдыхай')
					break
				default:
					ctx.reply(sendHomework())
					break
				}
			});
			await bot.startPolling((err) => {
				if (err) {
				console.error(err);
				}
			});
}
module.exports = BotVk;