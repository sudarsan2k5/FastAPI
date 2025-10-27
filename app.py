from fastapi import FastAPI, HTTPException
from model import Employee
from typing import List

app = FastAPI()

# In-memory "database"
employee_db: List[Employee] = []

# ✅ Read all employees
@app.get('/employee', response_model=List[Employee])
def get_all_employees():
    return employee_db


# ✅ Read a specific employee
@app.get('/employee/{emp_id}', response_model=Employee)
def get_employee(emp_id: int):
    for employee in employee_db:
        if employee.id == emp_id:
            return employee
    # You forgot to *raise* the exception here
    raise HTTPException(status_code=404, detail="Employee Not Found :( ")


# ✅ Add an employee
@app.post('/employee', response_model=Employee)
def add_employee(new_emp: Employee):
    for employee in employee_db:
        if employee.id == new_emp.id:
            raise HTTPException(status_code=400, detail="Employee Already Exists :)")
    employee_db.append(new_emp)
    return new_emp


# ✅ Update an employee
@app.put('/employee/{emp_id}', response_model=Employee)
def update_employee(emp_id: int, updated_emp: Employee):
    for index, employee in enumerate(employee_db):
        if employee.id == emp_id:
            employee_db[index] = updated_emp
            return updated_emp
    raise HTTPException(status_code=404, detail="Employee does not exist :(")


# ✅ Delete an employee
@app.delete('/employee/{emp_id}')
def delete_employee(emp_id: int):
    for index, employee in enumerate(employee_db):
        if employee.id == emp_id:
            del employee_db[index]
            return {"message": "Employee Deleted Successfully :) "}
    raise HTTPException(status_code=404, detail="Employee Not Found :(")
