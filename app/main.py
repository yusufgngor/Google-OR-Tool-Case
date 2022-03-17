
from fastapi import FastAPI
from app.Models.SolverModel import SolverModel

from app.Models.input_model import InputModel
from app.Logic.solver import solver


app = FastAPI()


@app.get("/")
def read_root():
    return {"Note": "To use Solver please send a post to /solver End point"}


@app.post("/solver/")
async def solve(inputModel: InputModel):
    model = SolverModel(inputModel)
    result = solver(model)
    return result
