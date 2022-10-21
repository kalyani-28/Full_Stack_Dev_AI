from fastapi import Depends, FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class FormModel(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...)
    ):
        return cls(username=username, password=password)


@app.post("/")
def main(form_data: FormModel = Depends(FormModel.as_form)):
    return form_data
