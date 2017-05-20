let CONFIG = {
  RABBITMQ_URI: process.env.RABBITMQ_URI || 'amqp://guest:guest@localhost:5672',
  SOCKET_PORT: process.env.SOCKET_PORT || 1333
} 

export default CONFIG