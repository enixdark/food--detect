let CONFIG = {
  RABBITMQ_URI: process.env.RABBITMQ_URI || 'amqp://guest:guest@localhost:5672',
  SOCKER_PORT: process.env.SOCKER_PORT || 1333
} 

export default CONFIG