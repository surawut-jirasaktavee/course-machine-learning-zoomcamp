FROM python:3.9.12-slim

WORKDIR /app

COPY images/ /app/images/

COPY ./.streamlit/ /app/.streamlit/

COPY ["Pipfile", "Pipfile.lock", "/app/"]

COPY app.py /app

RUN pip install pipenv

RUN pipenv install --system --deploy

EXPOSE 8501

# CMD streamlit run app.py

ENTRYPOINT ["streamlit", "run", "app.py"]