const { Client } = require("@notionhq/client")

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
