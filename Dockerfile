FROM python:3.11-slim

RUN \
  if [ "$TARGETARCH" = "arm64" ] ; \
  then \
  apt-get install -y wget unzip libc6-amd64-cross \
  && ln -s /usr/x86_64-linux-gnu/lib64/ /lib64; \
  fi

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# COPY ./data-science-utils/ ./data-science-utils/
# RUN pip install ./data-science-utils

WORKDIR app/

COPY ./data/ ./data/
COPY ./src/ ./src/
COPY ./app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
