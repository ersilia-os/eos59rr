FROM bentoml/model-server:0.11.0-py39
MAINTAINER ersilia

RUN conda install -c tmap tmap==1.0.6
RUN pip install rdkit==2024.9.6
RUN pip install biopython==1.78
RUN pip install biopandas==0.2.8
RUN pip install seaborn==0.13.2
RUN pip install umap-learn==0.3.10
RUN pip install python-highcharts==0.4.2
RUN pip install pandas==2.2.3
RUN pip install colored==1.3.93
RUN pip install colorlog==4.0.2
RUN pip install mordredcommunity[full]==2.0.6
RUN pip install gdown==4.4.0
RUN pip install mhfp==1.9.2
RUN pip install faerun==0.4.7
RUN pip install tqdm==4.67.1
RUN pip install scipy==1.13.1
RUN pip install numpy==1.26.4
RUN pip install numba==0.60.0
RUN pip install joblib==1.5.0
RUN pip install scikit-learn==0.24
RUN pip install lapjv==1.3.27

WORKDIR /repo
COPY . /repo

