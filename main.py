
from fastapi import FastAPI

from Models.input_model import InputModel
from solver import solver

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Worasdasaaald"}


@app.post("/solver/")
async def solver2(inputModel: InputModel):
    plan_output,max_route_distance = solver(inputModel)
    return plan_output
