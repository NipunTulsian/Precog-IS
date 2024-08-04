class Config:
    SECRET_KEY = 'aplhamu'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/precog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'nipun.tulsian.nt@gmail.com'
    MAIL_PASSWORD = 'enpt habp hhnq vikq'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    slots = [
        {"id":1,"slot":"Monday 10-12 am"},
        {"id":2,"slot":"Monday 3-5 pm"},
        {"id":3,"slot":"Tuesday 10-12 am"},
        {"id":4,"slot":"Tuesday 3-5 pm"},
        {"id":5,"slot":"Wednesday 10-12 am"},
        {"id":6,"slot":"Wednesday 3-5 pm"},
        {"id":7,"slot":"Thursday 10-12 am"},
        {"id":8,"slot":"Thursday 3-5 pm"},
        {"id":9,"slot":"Friday 10-12 am"},
        {"id":10,"slot":"Friday 3-5 pm"},
    ]