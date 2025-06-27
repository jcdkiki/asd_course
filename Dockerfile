FROM trampgeek/jobeinabox@sha256:2720e97aeb988fc2ce9f522845d264124ebc266f042f3619d0d5caf2f04037b2

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y gcc

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --break-system-packages

COPY pyproject.toml README.md ./
COPY main.py .
ENTRYPOINT ["python3", "main.py"]

COPY ./src ./src
RUN pip3 install --break-system-packages . && rm -r src requirements.txt pyproject.toml
