FROM python:3.11-slim
WORKDIR /code
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libegl1-mesa \
    libgl1-mesa-dri \
    mesa-utils \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 8501
CMD ["python","-m","streamlit","run","app.py"]