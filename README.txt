NLP understand
==============
Natural Language Processing (NLP) is a branch of Machine learning (ML) that is focused on making computers understand human language.
It is used to create language models, language translation apps like Google Translate, and virtual assistants, among other things.

Through this project, we interact with the chatbot via Human Language.
Dialogflow ES: Provides the standard agent type suitable for small and simple agents.
throughout agent will make conversation that is (intent)
Dialogflow algorithm will understand what you saying or what need to do.

creating intent
intent 1 = "New order"
intent 2 = "track order"

what we will give prompt into the intent it's responding.

Directory structure
===================
backend: Contains Python FastAPI backend code
db: contains the dump of the database. you need to import this into your MySQL db by using MySQL workbench tool
dialogflow_assets: this has training phrases etc. for our intent
frontend: website code

Install these modules
======================

pip install mysql-connector
pip install "fastapi[all]"

OR just run pip install -r backend/requirements.txt to install both in one shot

To start fastapi backend server
================================
1. Go to backend directory in your command prompt
2. Run this command: uvicorn main:app --reload

ngrok for https tunneling
================================
1. To install ngrok, go to https://ngrok.com/download and install ngrok version that is suitable for your OS
2. Extract the zip file and place ngrok.exe in a folder.
3. Open windows command prompt, go to that folder and run this command: ngrok http 80000

NOTE: ngrok can timeout. you need to restart the session if you see session expired message.
