
# BIKE SHARING DASHBOARD

## Setup Environment - Anaconda
conda create --name ds_project python 3.12.4
conda activate ds_project
pip install -r requirements.txt

## Setup Environment - Shell/Terminal
mkdir data_analysis
cd data_analysis
pipenv install
pipenv shell
pip install -r requirements.txt

## Run streamlit app
streamlit run Dashboard.py 

