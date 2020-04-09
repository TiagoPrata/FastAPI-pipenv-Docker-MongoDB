FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY requirements.txt /tmp
RUN pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org -r /tmp/requirements.txt
# RUN pip install -r /tmp/requirements.txt
WORKDIR /app
COPY ./app .
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]