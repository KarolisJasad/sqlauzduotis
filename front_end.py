import PySimpleGUI as sg
from datetime import datetime

from main import create_employee, get_employees, delete_employee, change_employee

headings=['Vardas', 'Pavardė', 'Gimimo data', 'Pareigos', 'Atlyginimas']

layout = [
    [sg.Text(headings[0], size=(15,1)), sg.Input(size=20,key='-NAME-')],
    [sg.Text(headings[1], size=(15,1)), sg.Input(size=20,key='-SURNAME-')],
    [sg.Text(headings[2], size=(15,1)), sg.Input(size=20,key='-BIRTHDATE-')],
    [sg.Text(headings[3], size=(15,1)), sg.Input(size=20,key='-POSITION-')],
    [sg.Text(headings[4], size=(15,1)), sg.Input(size=20,key='-SALARY-')],
    [sg.Button('Pridėti', key='-ADD-'), sg.Button('Peržiūrėti', key='-VIEWLIST-'), sg.Button('Redaguoti', key='-CHANGELIST-'), sg.Button('Išsaugoti', key='-SAVE-', disabled=True), sg.Button('Ištrinti', key='-DELETE-')],
    [sg.Table(values=[], headings=['ID', 'Vardas', 'Pavardė', 'Gimimo data', 'Pareigos', 'Atlyginimas', 'Isidarbinimo data'], key='-EMPLOYEES-', justification='left', auto_size_columns=False, col_widths=[3, 10, 10, 12, 17, 10, 15])]
]

window = sg.Window('Darbuotojų valdymas', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == '-ADD-':
        keys=['-NAME-', '-SURNAME-', '-BIRTHDATE-', '-POSITION-', '-SALARY-']
        input_values = [values[key] for key in keys]

        if all(input_values):
            try:
                birthdate = datetime.strptime(input_values[2], '%Y-%m-%d').date()
                create_employee(input_values[0], input_values[1], birthdate, input_values[3], input_values[4])
                sg.popup('Employee succesfully added!')
            except ValueError:
                sg.popup('Incorrect date format, please use this format: YYYY-MM-DD.')
        else:
            sg.popup('Please fill all the fields.')
        
        employees = get_employees()
        window['-EMPLOYEES-'].update([f'{e.id} {e.name} {e.surname} {e.birthdate} {e.position} {e.salary} {e.working_since}' for e in employees])

    if event == '-VIEWLIST-':
        employees = get_employees()
        window['-EMPLOYEES-'].update([f'{e.id} {e.name} {e.surname} {e.birthdate} {e.position} {e.salary} {e.working_since}' for e in employees])

    if event == '-CHANGELIST-':
        sg.popup('Enter new values you wish to change')
        selected_rows = values['-EMPLOYEES-']
        if selected_rows:
            selected_row_index = selected_rows[0]
            employees = get_employees()
            if selected_row_index < len(employees):
                employee = employees[selected_row_index]
                employee_id = employee.id
                for attribute, value in zip(['-NAME-', '-SURNAME-', '-BIRTHDATE-', '-POSITION-', '-SALARY-'], [employee.name, employee.surname, employee.birthdate, employee.position, employee.salary]):
                    window[attribute].update(value=value)
                window['-SAVE-'].update(disabled=False)
            else:
                sg.popup('Invalid selected row index.')
        else:
            sg.popup('Please select an employee from the list.')

    if event == '-SAVE-':
        if employee_id:
            name = values['-NAME-']
            surname = values['-SURNAME-']
            birthdate = values['-BIRTHDATE-']
            position = values['-POSITION-']
            salary = values['-SALARY-']

            if name or surname or birthdate or position or salary:
                try:
                    birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date() if birthdate else None
                    change_employee(employee_id, name=name, surname=surname, birthdate=birthdate, position=position, salary=salary)
                    employees = get_employees()
                    window['-EMPLOYEES-'].update([f'{e.id} {e.name} {e.surname} {e.birthdate} {e.position} {e.salary} {e.working_since}' for e in employees])
                    sg.popup('Employee information saved successfully!')
                except ValueError:
                    sg.popup('Incorrect date format, please use this format: YYYY-MM-DD.')
            else:
                sg.popup('No changes made.')
        else:
            sg.popup('Please select an employee from the list.')

    if event == '-DELETE-':
        selected_rows = values['-EMPLOYEES-']
        if selected_rows:
            selected_row_index = selected_rows[0]
            employees = get_employees()
            if selected_row_index < len(employees):
                employee = employees[selected_row_index]
                employee_id = employee.id
                delete_employee(employee_id)
                sg.popup('Employee deleted succesfully')
        employees = get_employees()
        window['-EMPLOYEES-'].update([f'{e.id} {e.name} {e.surname} {e.birthdate} {e.position} {e.salary} {e.working_since}' for e in employees])