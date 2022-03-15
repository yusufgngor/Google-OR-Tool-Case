
from fastapi import FastAPI
from Models.SolverModel import SolverModel

from Models.input_model import InputModel
from solver import solver

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Worasdasaaald"}


@app.post("/solver/")
async def solve(inputModel: InputModel):
    model = SolverModel(inputModel)
    result = solver(model)

    return result
