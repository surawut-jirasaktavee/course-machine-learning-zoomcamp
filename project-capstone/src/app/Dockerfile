FROM python:3.9.12-slim

WORKDIR /app

COPY .streamlit /app

COPY app.py /app

COPY ["Pipfile", "Pipfile.lock", "/app/"]

RUN pip install pipenv

RUN pipenv install --system --deploy

EXPOSE 8501

CMD streamlit run app.py