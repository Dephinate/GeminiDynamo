# QuizMaster
YouTubeFlashCard is an AI tool that generates flashcards by extracting key concepts, terms, and definitions from YouTube videos using gemini 1.5 pro at 95% lower cost and 90% lower processing time.

## Table of Contents

* [Overview](#overview)
  * [Brief Description](#brief-description)
  * [Technologies Used](#technologies-used)
  * [Target Audience](#target-audience)
  * [Project Status](#project-status)
  * [Future Plans](#future-plans)
* [Installation](#installation)
* [Usage](#usage)
* [Model and Data](#model-and-data)
* [How to authenticate GCP to access APIs?](#How-to-authenticate-GCP-to-access-APIs)
* [Contributing](#contributing)
* [Acknowledgments](#acknowledgments)
* [Contact](#contact)


## Overview
YouTubeFlashCard is an AI tool that generates flashcards by extracting key concepts, terms, and definitions from YouTube videos using gemini 1.5 pro at 95% lower cost and 90% lower processing time.
### Brief Description
QuizMaster is an AI powered quiz generator that can generate and assess Quizzes from any educational document with ease. User can upload any number of pdfs and enter the topic to generate quizzes and give the assessment. 
Say goodbye to manual quiz creation and hello to automated, efficient learning.

![Watch the video](data/dynamo.gif)

### Technologies used
+ Langchain, GCP, VertexAI, Gemini 1.5, React, HuggingFace

### Target Audience
+ Students
+ Teaching Assitants
+ Professors
+ Educators
+ E-Learning Platforms

### Project Status
+ Phase 1 : Currently the project works only for videos with transcripts.

### Future Scope
+ Extend the capabilities of the the application to support videos with and without timestamps and allow users to put timestamps.

## Installation
> ** Python 3.10**
1. Clone this repository to your local machine using:
    ```bash
    $ git clone https://github.com/Dephinate/GeminiDynamo.git
    $ cd your_project
    ```
2. Create a conda environment and install dependencies
    ```bash
    $ pip install -r requirements.txt
    ```

## Usage
1. Need to first perform google authentication to use Gemini pro from Vertex AI.
2. Open two terminals.
2. Copy the following command in terminal 1:
    ```bash
    $ cd frontend/dynamocards/
    $ npm run dev
    ```
3. Copy the following command in terminal 2:
    ```bash
    $ cd backend/
    $ python main.py
    ```

## Model and Data
LLM uses: Gemini 1.5 Pro from Vertex AI

## How to authenticate GCP to access APIs?
Watch the video : https://www.loom.com/share/fa6cd412c1274683a0ebab5a43b09597?sid=bff89143-0997-426d-81ee-c3f0feea549f

## Acknowledgments
https://www.linkedin.com/in/mikhail-ocampo/

https://python.langchain.com/v0.1/docs/get_started/introduction/

https://python.langchain.com/v0.1/docs/integrations/vectorstores/chroma/

https://python.langchain.com/v0.1/docs/expression_language/

https://colabdoge.medium.com/what-is-rag-retrieval-augmented-generation-b0afc5dd5e79

https://www.hopsworks.ai/dictionary/vector-database

## Contact
[LinkedIn] (https://www.linkedin.com/in/vks2102/)