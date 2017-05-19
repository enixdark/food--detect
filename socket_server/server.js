let server = require('http').createServer()
let io = require('socket.io')(server)
let amqp = require('amqplib/callback_api')
let config = require('./config')

console.log(config.default)
io.on('connection', (socket ) => {
  console.log('conection')
  client.on('event', (data) => {})
  client.on('disconnect', () => {})
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
      }, {noAck: true})
    })
  })
  })

server.listen(config.default.SOCKER_PORT, () => {
  console.log(`server listen ${config.default.SERVER_PORT}`)
})


