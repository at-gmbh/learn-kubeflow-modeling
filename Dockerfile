FROM tensorflow/tensorflow:2.1.0-gpu-py3
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/modeling /modeling
COPY src/pipeline_steps /
