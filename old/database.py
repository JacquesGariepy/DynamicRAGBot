from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

engine = create_engine('sqlite:///questions.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def save_question(question, answer):
    session = Session()
    new_question = Question(question=question, answer=answer)
    session.add(new_question)
    session.commit()
    session.close()

def get_recent_questions(limit=10):
    session = Session()
    questions = session.query(Question).order_by(Question.timestamp.desc()).limit(limit).all()
    session.close()
    return questions
