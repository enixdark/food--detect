let server = require('http').createServer()
let io = require('socket.io')(server)
let amqp = require('amqplib/callback_api')
let config = require('./config')

let clients = {}

io.on('connection', (client) => {
  client.send(client.id)
  clients[client.id] = client
  console.log('connection')
  client.on('disconnect', () => {

  })
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
          let id = JSON.parse(msg.content.toString().replace(/\'/g,"\"").replace("u\"","\""))["id"]
          
          clients[id].emit('answer', msg.content.toString())
        }, {noAck: true})
      })
    })
  })

server.listen(config.default.SOCKET_PORT, () => {
  console.log(`server listen ${config.default.SOCKET_PORT}`)
})


