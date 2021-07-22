const {Client} = require('pg')
const client = new Client({
	connectionString:'postgres://xbwoosfturwnmu:4f3f0a25361cac11df1af8a3dfe11469029a422f85e055fa1f6072cb1c4b48c3@ec2-54-73-68-39.eu-west-1.compute.amazonaws.com:5432/d4g1mkv1jennht',
	ssl:{
	    rejectUnauthorized: false
	}
});
client.connect()
console.log(client.query(
			'SELECT day, lesson, homework FROM public.homeworktable WHERE daynum=$1 and daymonth=$2 and dayyear=$3',
			[27, 4, 2021],  
			(err,res) => {
				if (err){
				console.log(err)
				return '@mezhendosina, чето сломамломсь'
				}///
				
				let i = 'Домаха на ' + res.rows[0].day +'\n\n' + res.rows.map(function(item){ return item.lesson + ": " + item.homework}).join("\n");
				console.log(i)
				client.end()
			}
			))