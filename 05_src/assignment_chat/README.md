# ActiveAge: AI Health & Cognitive Personal Coach
ActiveAge is an AI-based coaching agent designed to support users, especially seniors, in maintaining their physical and mental well-being. The goal of this app is to provide a simple, safe, and structured way for users to access daily exercises, mental activities, and health-related information.

## Core Services
This app is built using LangGraph and LangChain, and includes three main services. Each service uses a different data source and retrieval method.

### Service 1: Physical Fitness (Wger API)

This service is implemented through the ```get_body_exercise()``` tool in ```tools_exercise.py```.

It connects to the Wger REST API to retrieve exercise data. The tool processes the API response and returns:
- One exercise at a time
- Step-by-step instructions
- Simple and safe guidance suitable for seniors


### Service 2: Mental Activity (ChromaDB RAG)

This service is implemented through the ```get_mental_activity()``` tool in ```tools_mental.py```.

It uses a Retrieval-Augmented Generation (RAG) approach with a persistent ChromaDB vector database. The database is built from curated mental exercise content using OpenAI embeddings.

The tool performs semantic search to return:
- Cognitive exercises
- Brain training activities

The vector store is created by ```main_vector_db.py``` for scalable indexing.

### Service 3: Real-time Health Insights (Tavily AI Search)

This service is implemented through the ```get_web_search()``` tool in ```tools_search.py```.

It uses Tavily AI search to retrieve up-to-date information, such as:

- Health news
- Nutrition information
- Fitness trends

The results are formatted into clean, readable text before being returned.

## Features

### LangGraph-Based Architecture

I used a StateGraph architecture to manage the interaction between the model and tools. This allows:

- Multi-step reasoning
- Tool calling when needed
- Maintaining conversation history using MessagesState

### Modular Design

Each service is implemented as a separate tool, making the system easier to extend or modify later.

### User-Friendly Output

I enforced a step-by-step format for exercise instructions so that they are easier to follow, especially for seniors. I also kept the language simple and concise.

### Tool Output Handling

All tool outputs are converted into flat strings before being passed back to the model. This avoids issues with nested JSON objects and keeps the conversation flow stable.

### Safety Constraints

To keep the system focused, I added simple guardrails to block unrelated topics:

- Cats or dogs
- Horoscopes or zodiac signs
- Taylor Swift

### Basic Prompt Protection

The agent is designed to refuse requests that try to reveal system prompts or internal instructions.

## Summary

This project demonstrates how to combine:

- API-based data (Wger)
- Retrieval-based knowledge (ChromaDB)
- Real-time search (Tavily)

into a single agent using LangGraph.