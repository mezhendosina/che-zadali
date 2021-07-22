const { Client } = require('pg');

const client = new Client({
  connectionString: 'postgres://xbwoosfturwnmu:4f3f0a25361cac11df1af8a3dfe11469029a422f85e055fa1f6072cb1c4b48c3@ec2-54-73-68-39.eu-west-1.compute.amazonaws.com:5432/d4g1mkv1jennht',
  ssl: {
    rejectUnauthorized: false
  }
});
client.query('SELECT * FROM homeworktable', (err, res) => {
  console.log(err, res.rows[0])
  pool.end()
})