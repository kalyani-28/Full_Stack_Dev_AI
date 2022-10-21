import os
from pathlib import Path
from .formGenerator import generateFormCode, makeFormPath


def fastApiSetup():
    """FastApi app setup code"""
    code = """
import shelve
from fastapi import Depends, FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from starlette.responses import FileResponse
import starlette.status as status

app = FastAPI()
    """
    return code


def staticFolderSetup():
    code = f'app.mount("/static", ' + \
        f'StaticFiles(directory="static"), name="static")'
    return code


def templateSetup():
    return 'templates = Jinja2Templates(directory="templates")'


def exceptionHandlers():
    code = """
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return RedirectResponse("/404")
    """
    return code


def get404():
    code = """
@app.get("/404")
async def main():
    return FileResponse("static/404.html")
    """
    return code


def getIndex(forms):
    code = """
@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", context=
        {{
            "request": request,
            "forms": {0}
        }}
    )
    """
    return code.format(forms)


def getData():
    code = """
@app.get("/data/{formId}")
async def main(request: Request, formId: str):
    shelf = shelve.open("appData.db", flag="c")
    data = []
    try:
        if shelf.__contains__(formId):
            data = shelf[formId]
    finally:
        shelf.close()
        
    print(data)
    return templates.TemplateResponse("data.html", context=
        {
            "request": request,
            "data": data
        }
    )
    
    """
    return code


def formId(id):
    return f'form{id}'


def htmlContainer(body):
    code = """
<!doctype html>
<html>
<head>
    <title>Form</title>
    <meta name="keywords" content="html tutorial template">
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
</head>
<body>
    <nav class="navbar navbar-light bg-light">
        <a class="navbar-brand" href="/">Home</a>
    </nav>
    {0}
</body>
</html> 
    """
    return code.format(body)


def htmlTemplate():
    template = """
    <div class="container my-3">
    <div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">Form</div>
            <div class="card-body">
                <form action="{{actionPath}}" method="POST">
                    {% for _, elem in elements | dictsort -%}
                    {% set label = elem["label"].replace(" ", "_") %}
                    <div class="form-group row mb-3">
                        <label for="{{label}}" class="col-form-label col-md-4 text-md right">
                            {{label}}:
                        </label>
                        <div class="col-md-6">
                            <input type="{{elem["type"]}}" id="{{label}}" name={{label}} class="form-control" required="required"/>
                        </div>
                    </div>
                    {% endfor -%}
                    <div class="form-group row">
                        <div class="col-md-6 offset-md-4">
                            <button type="submit" class="btn btn-primary">Submit</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
    </div>
    </div>
    """
    return template


def indexTemplate():
    template = """
    <div class="container my-3">
    <div class="row justify-content-center">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">Form ID</th>
                    <th scope="col">Link</th>
                    <th scope="col">Data</th>
                </tr>
            </thead>
            
            {% for _ in forms -%}
                <tbody>
                    <tr>
                        <th scope="row">form{{loop.index0}}</th>
                        <td><a href="/form{{loop.index0}}">access form</a></td>
                        <td><a href="/data/form{{loop.index0}}">access data</a></td>
                    </tr>
                </tbody>
            
            {% endfor -%}
            
        </table>
    </div>
    </div>   
    """
    return template


def dataViewTemplate():
    template = """
    <div class="container my-3">
    <div class="row justify-content-center">
        {% if not data %}
        <h2>No entries have been submitted</h2>
        {% else %}
        <h2>Form entries</h2>
           <table class="table">
            <thead>
                <tr>
                    <th scope="col">Entry #</th>
                    {% for key, _ in data[0].items() -%}
                        <th scope="col">{{key}}</th>
                    {% endfor -%}
                </tr>
            </thead>
            
            {% for entry in data -%}
                <tbody>
                    <tr>
                        <th scope="row">{{loop.index}}</th>
                        {% for _, val in entry.items() -%}
                            <td>{{val}}</td>
                        {% endfor -%}
                    </tr>
                </tbody>
            {% endfor -%}
            
        </table>     
        {% endif %}
    </div>
    </div>
    """
    return template


def html404():
    html = """
<div class="d-flex justify-content-center align-items-center" id="main">
    <h1 class="mr-3 pr-3 align-top border-right inline-block align-content-center">404</h1>
    <div class="inline-block align-middle">
    	<h2 class="font-weight-normal lead" id="desc">The page you requested was not found.</h2>
    </div>
</div>
    """
    return html


def pipRequirements():
    return """
#
# These requirements were autogenerated by pipenv
# To regenerate from the project's Pipfile, run:
#
#    pipenv lock --requirements
#

-i https://pypi.python.org/simple
anyio==3.5.0; python_full_version >= '3.6.2'
asgiref==3.5.0; python_version >= '3.7'
click==8.0.4; python_version >= '3.6'
fastapi==0.75.0
h11==0.13.0; python_version >= '3.6'
httptools==0.4.0
idna==3.3; python_version >= '3.5'
jinja2==3.0.3
markupsafe==2.1.0; python_version >= '3.7'
numpy==1.22.3; python_version >= '3.8'
opencv-python==4.5.5.64
pydantic==1.9.0; python_full_version >= '3.6.1'
python-dotenv==0.19.2
python-multipart==0.0.5
pyyaml==6.0
six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'
sniffio==1.2.0; python_version >= '3.5'
starlette==0.17.1; python_version >= '3.6'
typing-extensions==4.1.1; python_version >= '3.6'
uvicorn[standard]==0.17.6
watchgod==0.7
websockets==10.2
    """


def readme():
    return """
1. Install python requirements from requirements.txt
2. Run uvicorn app:app in project folder
3. Access website at localhost:8000
"""


def generateApi(forms):
    """Generate web app. Project files written to results/webApp"""

    # create project folders
    root = os.path.dirname(__file__)
    projectRoot = os.path.join(root[:root.rfind("/src/")], "results/webApp")
    print(projectRoot)

    staticFolder = os.path.join(projectRoot, "static")
    templateFolder = os.path.join(projectRoot, "templates")
    [Path(p).mkdir(parents=True, exist_ok=True)
     for p in [projectRoot, staticFolder, templateFolder]]

    # get backend api code for each form
    formCodeBlocks = [generateFormCode(formId(idx), form)
                      for idx, form in enumerate(forms)]

    # write html template to templates folder
    with open(os.path.join(templateFolder, "template.html"), "w") as templateFile:
        templateFile.write(htmlContainer(htmlTemplate()))

    # write index page template to templates folder
    with open(os.path.join(templateFolder, "index.html"), "w") as indexFile:
        indexFile.write(htmlContainer(indexTemplate()))

    # write data view template to templates folder
    with open(os.path.join(templateFolder, "data.html"), "w") as dataTemplateFile:
        dataTemplateFile.write(htmlContainer(dataViewTemplate()))

    # write 404 html to static folder
    with open(os.path.join(staticFolder, "404.html"), "w") as html404File:
        html404File.write(htmlContainer(html404()))

    # create backend api by appending the code for each form to fastApi app setup code
    formCode = "\n".join(formCodeBlocks)
    apiCode = "\n".join([fastApiSetup(), staticFolderSetup(),
                         templateSetup(), exceptionHandlers(), formCode,
                         get404(), getIndex(forms), getData()])
    # write backend code to project folder
    with open(os.path.join(projectRoot, "app.py"), "w") as appFile:
        appFile.write(apiCode)
    # write pip file to project folder
    with open(os.path.join(projectRoot, "requirements.txt"), "w") as pipFile:
        pipFile.write(pipRequirements())
    # write readme to project folder
    with open(os.path.join(projectRoot, "readme.txt"), "w") as readmeFile:
        readmeFile.write(readme())


if __name__ == "__main__":
    form1 = {
        "1": {"label": "username", "type": "text"},
        "2": {"label": "password", "type": "text"},
        "3": {"label": "full name", "type": "text"}
    }

    form2 = {
        "1": {"label": "screen name", "type": "text"},
        "2": {"label": "secret code", "type": "text"},
        "3": {"label": "captcha", "type": "text"}
    }

    generateApi([form1, form2])
