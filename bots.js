const {Client} = require('pg')
const VkBot = require('node-vk-bot-api');
const { Client } = require("@notionhq/client")

const client = new Client()
await client.connect()

async function sendHomework() {
	var date = new Date()
	async function selectHomework(day=date.getDay()+1, date=date.getDate()+1){
		return await client.query("SELECT day, lesson, homework WHERE dayName='$1' and dayNum='$2' and dayMonth='$3' and dayYear='$4'", [day, date, date.getMonth(), date.getYear()], (err,res) => {
				if err{
				console.log(err)
				return '@mezhendosina, чето сломамломсь, отправил тебе  ̶̶̶х̶у̶й̶ логи за щеку :)'
				}
				return '''Домаха на ${client.query("select day WHERE dayName=$1 and dayNum=$2 and dayMonth=$3 and dayYear=$4", [day, date.getDate()+1, date.getMonth(), date.getYear()]} \n\n''' + res.rows.map(function(item){ return item.lesson + ": " + item.homework}).join("\n");
	}
	switch (date.getDay()) {
		case 6:
			let homework1 = selectHomework(6, date.getDate())
			let homework2 = selectHomework(1, date.getDate()+2)
			return homework1 + homework2
		default:
			return selectHomework()
			}
	}
async function addHomeworkToNotion (nameHomewok, lesson) {
		const notion = new Client({
			auth: 'secret_FDBc6pzcRviubDPD74eB9Hkhkyd2ZEi4Ist2oyqQksO',
		});

		const response = await notion.pages.create({
			parent: {
				database_id: '5f6926e375844a7db3a1fc0fefa2d7ad',
			},
			properties: {
				'Задание': {
					title: [{
						text: {
							content: nameHomewok,
						},
					},
					]
				},
				'Status': {
					select: {
						name: 'Скоро сдавать',
					},
				},
				'Предмет': {
					select: {
						name: lesson,
					}
				},
			}
		});
		console.log(response);
	}

async function vkBot() {
		const bot = new VkBot('a9fc970aabe2a7043e253216e66889c81c9f79bc597f15c1c629cfc5ea96760d3c962645be7327b86f6a3');

		bot.command('/', (ctx) => {
			ctx.reply('/');
		});

		bot.command('Че задали', (ctx) => {
			await client.query('SELECT day, lesson, homework WHERE dayName="$1"  FROM homeworkTable', [selectday](err, res) => {
				res.rows.map()
			})
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
module.exports = vkBot;