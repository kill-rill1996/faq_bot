from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship, backref

from database.database import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    tg_id = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True, nullable=False)

    subgroups = relationship("SubGroup", back_populates="group")

    def __repr__(self):
        return f'{self.id}. {self.title}'


class SubGroup(Base):
    __tablename__ = 'subgroups'

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)

    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("Group", back_populates="subgroups")

    questions = relationship("Question", back_populates="subgroup")

    def __repr__(self):
        return f'{self.id}. Группа: {self.group.title} подгруппа: {self.title}'


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True, nullable=False)

    subgroup_id = Column(Integer, ForeignKey('subgroups.id'))
    subgroup = relationship("SubGroup", back_populates="questions")

    answers = relationship("Answer", back_populates="question")

    def __repr__(self):
        return f'{self.id}. {self.title}'


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)

    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship("Question", back_populates="answers")

    def __repr__(self):
        return f'{self.id}. {self.question.title} {self.text}'
