from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from dbms import students, StudentNotFound
from models import Student, UpdateStudent

app = FastAPI()

@app.exception_handler(StudentNotFound)
def student_not_found_handler(request: Request, exc: StudentNotFound):
    return JSONResponse(
        status_code=404,
        content={"message": f"Student with ID {exc.student_id} not found."},
    )

@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    students.append(student.model_dump())
    return {"message": "Student added successfully", "data": student}

@app.get("/students")
def get_all_students():
    return {"message": "List of all students", "data": students}

@app.patch("/students/{student_id}")
def partial_update_student(student_id: int, student: UpdateStudent):
    if student_id < 0 or student_id >= len(students):
        raise StudentNotFound(student_id)
    updated_data = student.model_dump(exclude_unset=True)
    students[student_id].update(updated_data)
    return {"message": "Student updated successfully", "data": students[student_id]}
