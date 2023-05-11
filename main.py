from darbuotojai_db import engine, Employee
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def create_employee(name, surname, birthdate, position, salary):
    employee = Employee(name=name, surname=surname, birthdate=birthdate, position=position, salary=salary)
    session.add(employee)
    session.commit()

def get_employees():
    employees = session.query(Employee).all()
    return employees

def change_employee(employee_id, **kwargs):
    employee = session.query(Employee).filter(Employee.id == employee_id).first()
    if employee:
        for key, value in kwargs.items():
            if hasattr(employee, key):
                setattr(employee, key, value)
        session.commit()

def delete_employee(employee_id):
    employee = session.query(Employee).filter(Employee.id == employee_id).first()
    if employee:
        session.delete(employee)
        session.commit()

# create_employee("Petras", "Petraitis", datetime(1998, 7, 14), "Programuotojas", "1500")