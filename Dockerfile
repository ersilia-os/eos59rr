FROM bentoml/model-server:0.11.0-py37
MAINTAINER ersilia

RUN pip install tmap==1.2.1
RUN pip install rdkit==2023.3.2
RUN wget https://raw.githubusercontent.com/ersilia-os/eos59rr/main/model/framework/code/bidd-molmap/requirements.txt
RUN pip install -r requirements.txt

WORKDIR /repo
COPY . /repo

