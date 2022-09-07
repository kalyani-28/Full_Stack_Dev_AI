FROM python:3.9
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /4990App
RUN git clone -q "https://gitlab.cs.uwindsor.ca/renau11s/4990-project.git" .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt
RUN pip uninstall --yes opencv-python
RUN pip install opencv-python-headless
ADD ./gcp-auth.json .

WORKDIR /4990App/src
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]