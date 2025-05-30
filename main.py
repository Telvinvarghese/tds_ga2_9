import csv
import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Middleware for CORS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_student_data(file_path: str):
    """Reads student data from a CSV file."""
    students_data = []
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                students_data.append(
                    {"studentId": int(row["studentId"]), "class": row["class"]}
                )
        return students_data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error reading file: {str(e)}")


@app.get("/api")
async def get_students(class_: list[str] = Query(default=None, alias="class")):
    """Fetch all students or filter by class(es)."""
    file_path = os.path.join(os.getcwd(), "uploads", "q-fastapi.csv")
    students_data = read_student_data(file_path)

    if class_:
        filtered_students = [
            student for student in students_data if student["class"] in class_
        ]
        return JSONResponse(content={"students": filtered_students})

    return JSONResponse(content={"students": students_data})
