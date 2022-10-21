from jinja2 import Template


def generateFormCode(formName, elements):

    # generate back end code
    formModelClassName = formName + "Model"
    formClass = generateFormClass(elements, formModelClassName)
    formPath = makeFormPath(formName)
    formPostRoute = generateFormPostRoute(
        formModelClassName, formPath, formName)
    formGetRoute = generateFormGetRoute(formPath, elements)
    formCode = '\n'.join([formClass, formPostRoute, formGetRoute])

    return formCode


def makeFormPath(formName):
    return f'/{formName}'


def generateFormClass(elements, className):
    """Generates a fastApi form class with class name className
    and form elements from elements"""

    template = """
class {{className}}(BaseModel):

    {% for _, elem in elements | dictsort -%}
    {{elem["label"] | replace(" ", "_")}}: str
    {% endfor %}

    @classmethod
    def as_form(
        cls,
        {% for _, elem in elements | dictsort -%}
        {{elem["label"] | replace(" ", "_")}}: str = Form(...){{ "," if not loop.last else "" }}
        {% endfor -%}
    ):
        return cls(
            {% for _, elem in elements | dictsort -%}
            {{elem["label"] | replace(" ", "_")}}={{elem["label"] | replace(" ", "_")}}{{ "," if not loop.last else ""}}
            {% endfor -%}
        )
    """
    FormTemplate = Template(template)
    FormCode = FormTemplate.render(elements=elements, className=className)
    return FormCode


def generateFormPostRoute(className, routePath, formName):
    """Generate a fastApi form route for form class className with api path routePath"""

    template = """
@app.post("{{routePath}}")
def main(form_data: {{className}} = Depends({{className}}.as_form)):
    shelf = shelve.open("appData.db")
    try:
        if not shelf.__contains__("{{formName}}"):
            shelf["{{formName}}"] = []
            
        entries = shelf["{{formName}}"]
        entries.append(form_data.dict())
        shelf["{{formName}}"] = entries
    finally:
        shelf.close()
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    """
    routeTemplate = Template(template)
    routeCode = routeTemplate.render(
        className=className, routePath=routePath, formName=formName)
    return routeCode


def generateFormGetRoute(routePath, elements):
    template = """
@app.get("{{routePath}}", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("template.html", context= 
        {
            "request": request,
            "actionPath": "{{routePath}}",
            "elements": {{elements}}
        }
    )
    """

    return Template(template).render(routePath=routePath, elements=elements)
