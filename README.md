# LUMOS Project

## Table of contents

  - [Description](#description)
  - [Setup](#setup)
    - [Create Azure Service](#create-azure-service)
  - [Usage](#usage)
    - [Speech to Text](#speech-to-text)
    - [Sentiment Analysis](#sentiment-analysis)
    - [Dashboard](#dashboard)
  - [Dockerization](#dockerization)
  - [Results](#results)

## Description

Our project aims to predict customer satisfaction with customer service by detecting user feedback in their conversations. The workflow for this project involves converting speech to text and analyzing the sentiment of the text. If the sentiment score is high and positive, it indicates that the customer is satisfied with the service, whereas a low score suggests otherwise. This approach can be applied in various scenarios such as call centers and provides valuable insights into customer feedback and satisfaction levels.

One of the key features of this app is the inclusion of a name entity recognition module, which masks sensitive privacy information of the customers. This ensures that the privacy of the customers is protected while still allowing for accurate sentiment analysis.

The output of the sentiment analysis app includes the overall sentiment of the input file as well as its variation over time. This data is plotted in a graphical format that can be easily interpreted and used. By providing actionable insights into call center performance, this app can help organizations improve customer satisfaction and ultimately drive business success.


## Setup
To create the environment with the name specified in the environment file (team-scale-env), run the following line of code:

```bash
make setup-environment
```

### Create Azure Service

As we are using the Microsoft Azure SDK in this project, we need to create a Cognitive Speech Service in Azure. By using its key, resource region, and endpoint, we can provide service in Python. The key, resource region, and endpoint will be saved in a .env file to link to the Azure service in code.
<p align="center">
<img height="300" alt="Screen Shot 2023-04-27 at 18 11 52" src="https://user-images.githubusercontent.com/48161724/235016242-3c1cd501-b86f-48e8-be7c-2afbcd9a46fc.png">
  <img height="300" alt="Screen Shot 2023-04-27 at 18 17 52" src="https://user-images.githubusercontent.com/48161724/235018980-25f00eeb-a63e-4341-bafe-c538968515bb.png"><br>
  Create Azure Service
<p>

## Usage

Activate the environment with the following code:

```bash
source activate team-scale-env
```
 and then run 
 
 ```bash
 python -m spacy download en_core_web_sm
 ```
 
### Speech to Text

The audio data is stored in the data folder, and the transcribed script will be saved in an out.txt file. The Speech-to-Text conversion can be started by running the following command:
```bash
python -m speech_to_text/speech_to_text.py
```
<p align="center">
  <img width="422" title="audio example" alt="audio example" src="https://user-images.githubusercontent.com/48161724/235021334-a3b9d519-6574-4412-a5bb-91b935bcb89e.png"><br>
  Audio Example
 <p>
    
### Sentiment Analysis
To analyze the sentiment of the acquired text, execute the following command:
```bash
python -m sentiment_analysis/sentiment_analysis.py
```
We also analyze different parts of the audio to track changes in the client's attitude. This allows us to determine if the client's requirements have been satisfied. For example, a long audio will be equally split into four parts by time. If the service is solving the client's problem step by step, the client's satisfaction should gradually increase, with the final stage satisfaction being higher than the previous stages.
<p align="center">
  <img width="422" title="audio example" alt="audio example" src="https://user-images.githubusercontent.com/48161724/235025999-d4ec9b24-2e32-4de5-9b35-6bc67fee2208.png">
  <br>
  Customer Satisfaction
 <p>

### Dashboard
We have developed an interactive dashboard to help users easily analyze the text by inputting it or analyze the audio by loading it.
<p align="center">
   <img width="1460" alt="Screen Shot 2023-04-27 at 8 51 22 PM" src="https://user-images.githubusercontent.com/55615235/235046507-eba62862-ede5-4421-b6fd-33821de36416.png">
    <br>
  Dashboard
 <p>

## Dockerization
In order to build the Docker image, please follow the following steps:
1. Build the Docker image:
```bash
- docker build -t streamlit .
```
5. Run Docker image locally:
```bash
docker run -p 8501:8501 streamlit
```
    - The -p flag publishes the container’s port 8501 to your server’s 8501 port. Please change it accordingly if it has been changed in the Dockerfile.

### Toolkits: Azure

### Data Source: 
The data utilized in this project comprises publicly available audio files sourced from the internet. Some of the audio files have a clear positive or negative sentiment.

#### Recommended Sources: 
City of Edmonton: https://data.calgary.ca/

City of Calgary: https://data.calgary.ca/ 

G o A: https://regionaldashboard.alberta.ca/#/ 

#### Additional Sources:
[Demo Data Resources Kit](https://github.com/amtwo/Data-Blogger-Resource-Kit/wiki/Demo-data-repositories-&-Mock-data-creation)


