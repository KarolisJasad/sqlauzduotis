from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, mapped_column

engine = create_engine('sqlite:///employee.db', echo=False)

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False)
    surname = mapped_column(String(50), nullable=False)
    birthdate = mapped_column(Date, nullable=False)
    position = mapped_column(String(50), nullable=False)
    salary = mapped_column(Integer, nullable=False)
    working_since = mapped_column(Date, default=datetime.now().date())

    def __init__(self, name, surname, birthdate, position, salary):
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.position = position
        self.salary = salary
    
    def __repr__(self):
        return f"{self.id} {self.name} {self.surname} {self.birthdate} {self.position} {self.salary}"

Base.metadata.create_all(engine)



