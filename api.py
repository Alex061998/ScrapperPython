from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Line(BaseModel):
    matter: str
    teacher: str
    coef: float
    ects: float
    cc1: float
    cc2: float
    exam: float


app = FastAPI()


@app.get("/grades")
def grades():
    with open("exportFIles/note.txt", "r") as file:
        return file.readlines()


@app.get("/grades/{matter}")
def grades_by_matter(matter):
    with open("exportFIles/note.txt", "r") as file:
        for line in file.readlines():
            if matter in line:
                values = line[line.find(".00") + 9:line.find("\n")]
                if values == "":
                    raise HTTPException(status_code=404, detail="No grades in this matter.")

                average = calculate_average(values)
                values = values.split()
                values = [v.replace(',', '.') for v in values]
                vals_float = [float(v) for v in values]
                return {"grades": vals_float, "average": average}
        raise HTTPException(status_code=404, detail="This matter doesn't exist.")


def calculate_average(values: str) -> float:
    vals = values.split()
    vals = [v.replace(',', '.') for v in vals]
    vals_float = [float(v) for v in vals]
    average = sum(vals_float) / len(vals_float)
    average_rounded = round(average, 2)
    return average_rounded


@app.get("/grades/semester/{semester}")
def gradesBySemester(semester):
    with open("exportFIles/note.txt", "r") as file:
        matter_values = 0
        count = 0
        for line in file.readlines():
            if semester in line:
                coef_str = line[line.find(".00") - 1:line.find(".00") + 3]
                if coef_str != "":
                    coef = float(coef_str.split()[0]) if coef_str.split()[0].isdigit() else 0.0

                    values = line[line.find(".00") + 9:line.find("\n")]
                    if values == "":
                        raise HTTPException(status_code=404, detail="No grades in this semester.")

                    average = calculate_average(values)
                    for _ in range(int(coef)):
                        matter_values += average
                        count += 1
        return {"average": round(matter_values / count, 2) if count != 0 else 0.0}
