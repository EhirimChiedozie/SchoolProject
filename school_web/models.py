from sqlalchemy import Column,String,Integer,DateTime,Boolean
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from school_web import Base,login_manager,app,session
import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return session.query(Student).get(int(user_id))
    #return Student.query.get(int(user_id))

class Student(Base,UserMixin):
    __tablename__ = 'student'
    id = Column(Integer,primary_key=True)
    surname = Column(String(30),nullable=False)
    firstname = Column(String(30),nullable=False)
    middlename = Column(String(18),nullable=False)
    gender = Column(String(100),nullable=False)
    phonenumber = Column(String(18),unique=True,nullable=False)
    email = Column(String(100),unique=True,nullable=False)
    country = Column(String(50),nullable=False)
    state = Column(String(19),nullable=False)
    date_of_birth = Column(String,nullable=False)
    date_of_registration = Column(DateTime,default=datetime.datetime.utcnow)
    username = Column(String(50),unique=True,nullable=False)
    password = Column(String(30),nullable=False)
    confirmed = Column(Boolean,default=False)
    def __repr__(self):
        return f'''Student('{self.surname}', '{self.firstname}', '{self.middlename}','{self.gender}',
        '{self.phonenumber}','{self.email}','{self.country}','{self.state}',
        '{self.date_of_birth}','{self.date_of_registration}','{self.username}','{self.password}','{self.confirmed}')'''

    def get_reset_token(self,expires_sec=1800):
        s = serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return session.query(Student).get(user_id)