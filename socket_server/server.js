let http = require('http')
let server = http.createServer()
let io = require('socket.io')(server)
let amqp = require('amqplib/callback_api')
let config = require('./config')
let R = require('ramda')
let request = require('request')

let clients = {}
let URI = process.env.GOOGLE_SERIVCE_URI || 'http://0.0.0.0:6000/search'
let RECIPE_DETECT_URI = process.env.DETECT_SERVICE_URI || 'http://0.0.0.0:10000/search'

io.on('connection', (client) => {
  client.send(client.id)
  clients[client.id] = client
  console.log('connection')
})

amqp.connect(config.default.RABBITMQ_URI, (err, conn) => {
    conn.createChannel(function(err, ch){
      var ex = 'logs'
      ch.assertExchange(ex, 'fanout', {durable: false})

      ch.assertQueue('', {exclusive: true}, function(err, q) {
        console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", q.queue)
        ch.bindQueue(q.queue, ex, '')
        ch.consume(q.queue, function(msg) {

          console.log(" [x] %s", msg.content.toString())
          let dt = JSON.parse(msg.content.toString().replace(/\'/g,"\"").replace("u\"","\""))
          let id = dt['id']
          let obj = R.filter((v,k) => typeof v == 'number', dt)
          let data = Object.keys(obj).reduce(function(a, b){ return obj[a] > obj[b] ? a : b })
          // clients[id].emit('answer', msg.content.toString())
          request(`${URI}?query=${data}`,(error, response, body)  => {
            if(err) return 
            clients[id].emit('answer', JSON.stringify({name: data, context: body}))           
          })

          request(`${RECIPE_DETECT_URI}?query=${data}`,{ timeout: 30000}, (error, response, body)  => {
            if(err) return 
            clients[id].emit('nutrition', JSON.stringify({context: body}))           
          })
        }, {noAck: true})
      })
    })
  })

server.listen(config.default.SOCKET_PORT, () => {
  console.log(`server listen ${config.default.SOCKET_PORT}`)
})


