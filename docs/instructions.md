
#############################################################################################
############################################ PART 1 #########################################
#############################################################################################

#################################
# Step 1: Create Resource Group #
#################################

Subscription Name - Azure subscription 1

RG Group - abindev-rg

#################################
## Step 2: Create Azure OpenAI ##
#################################

Name - abinlabs

Tags:

rag-platform : dev

# 1. What are the Endpoint and Keys?
# Endpoint: 
https://abin2labs.openai.azure.com/

This is the URL your application uses to send requests to Azure OpenAI.

# API Key

Azure provides Key 1 and Key 2.

# Example usage:

    from openai import AzureOpenAI
    
    client = AzureOpenAI(
        api_key="YOUR_KEY",
        api_version="2024-02-01",
        azure_endpoint="https://abinlabs.openai.azure.com/"
    )

# Your FastAPI application will later use:

Endpoint → where to send requests
API Key → authentication
Deployment Name → which model to use

Think of it like:

    Your FastAPI App
          |
          | API Key
          |
          v
    https://abinlabs.openai.azure.com/
          |
          +--> gpt-4o-mini deployment
          +--> text-embedding-3-small deployment



# 2. Why Can't You Use It Yet?

Creating the Azure OpenAI resource only creates the service.

You still need to deploy actual models.

At this moment:

    Azure OpenAI Resource
    ✓ Exists
    
    GPT Model
    ✗ Not deployed
    
    Embedding Model
    ✗ Not deployed

Without model deployments, API calls will fail.

# 3. Where to Deploy Models?

Go to: Azure OpenAI Studio or https://ai.azure.com

# 4. Create a Project in AI Foundry

project name: abinsinghrajan-4017
foundry resource: abinsinghrajan-4017-resource

# 5. Deploy the Embedding Model

text-embedding-3-small

project endpoint: https://abinsinghrajan-4017-resource.services.ai.azure.com/api/projects/abinsinghrajan-4017
azure openai endpoint: https://abinsinghrajan-4017-resource.openai.azure.com/openai/v1

Target URI: https://abinsinghrajan-4017-resource.services.ai.azure.com


# Deploy the chat model

gpt-4o-mini

Target URI: "https://abinsinghrajan-6896-resource.services.ai.azure.com/openai/v1"



##################################
# Step 3: Create Azure AI Search #
##################################

Service name: abinlabs-aisearch

URI: https://abinlabs-aisearch.search.windows.net


##################################
# Step 4: Create Storage Account #
##################################
name: abinlabsstore
connection string = DefaultEndpointsProtocol=https;AccountName=abinlabsstore;AccountKey=exkEzZTL+EfAsOeYjQ0E9+UJObShdi2qF5puuwgscA4RWk6EILRk0dmcW6mkNlFB3S+Zu7OTWtmJ+AStdsHfTw==;EndpointSuffix=core.windows.net


# Part 1 Summary
    Azure AI Foundry           ✓
    GPT-4o-mini                ✓
    Embedding Model            ✓
    API Key Authentication     ✓
    Bearer Token Authentication✓
    Chat API Test              ✓
    Embedding API Test         ✓
    Storage Account            ✓
    Blob Container             ✓
    Storage Key Rotation       ✓

#############################################################################################
############################################ PART 2 #########################################
#############################################################################################
# Data Ingestion
# Part 2 Goal

    By the end of Part 2, you will have:
    
    Local PDF
        ↓
    Azure Blob Storage
        ↓
    Python Download
        ↓
    Extract Text
        ↓
    Split into Chunks

# 1. Create blob service
# 2. Create pdf service
# 3. Create chunk service
# 4. Create Upload PDF
# 5. Create Download PDF
# 6. Test PDF
# 7. Test Chunk

#############################################################################################
############################################ PART 3 #########################################
#############################################################################################

Current Architecture
    PDF
       ↓
    Azure Blob Storage
       ↓
    Python
       ↓
    Extract Text
       ↓
    Chunk Text
       ↓
    ?????????
Part 3 will fill that gap.

# Part 3 Goal
    
    By the end of Part 3, you will have:
    
    Chunks
       ↓
    Generate Embeddings
       ↓
    Create Azure AI Search Index
       ↓
    Store Embeddings
       ↓
    Perform Vector Search
    
    This is the core of RAG.

# 1. Create embedding Service
# 2. Create Search Service
# 3. Create Index (part of search)

# PART 3 # Phase 2

    Chunks
       ↓
    Generate Embeddings
       ↓
    Upload to Azure AI Search
       ↓
    User Question
       ↓
    Generate Question Embedding
       ↓
    Vector Search
       ↓
    Return Top K Chunks
# 1. Update search service 
We need two clients:
    SearchIndexClient
    SearchClient)

And Upload Documents
    Vector Search Method

# 2. Update ingest


#############################################################################################
############################################ PART 4 #########################################
#############################################################################################

                    User Question
                         │
                         ▼
          Generate Question Embedding
                         │
                         ▼
                Azure AI Search
                         │
                  Top K Chunks
                         │
                         ▼
                  Build Prompt
                         │
                         ▼
                    GPT-4o-mini
                         │
                         ▼
                     Final Answer

# 1. Create Chat Service
# 2. Create RAG Service
# 3. Create FAST API

Your Current Enterprise Architecture
                         User
                          │
                          ▼
                       FastAPI
                          │
                          ▼
                    RAG Service
                          │
        ┌─────────────────┼─────────────────┐─────────────────┐
        │                 │                 │                 │
        ▼                 ▼                 ▼                 ▼
Embedding Service   Search Service   Chat Service       Blob Service (Store PDF's)
        │                 │                 │
        ▼                 ▼                 ▼
Azure AI Foundry       Azure AI Search    AI Foundry
   (Embeddings)        (Vector Index)    (GPT 4o mini)
        │
        ▼
text-embedding-3-small


#############################################################################################
############################################ PART 5 #########################################
#############################################################################################

# Dockerize Application
    docker build -t azure-rag:v1 .
    docker run -p 8000:8000 azure-rag:v1
# to pass the env file
    docker run --env-file .env -p 8000:8000 azure-rag:v1

# create AKS cluster

# Create ACR
    # Tag image
    docker tag azure-rag:v1 akspracticeacr26abin.azurecr.io/azure-rag:v1

    # Push image
    docker push akspracticeacr26abin.azurecr.io/azure-rag:v1

    # Attach ACR to AKS
    az aks update --resource-group abindev-rg --name aks-practice-cluster --attach-acr akspracticeacr26abin

# Create kubernetes secrets
    kubectl create secret generic rag-secrets --from-env-file=.env

# Create Deployment YAML
# Create Service YAML
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml

# Current Architecture
                Users
                  │
                  ▼
              FastAPI
                  │
                  ▼
             AKS Cluster
                  │
                  ▼
             RAG Service
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
Embeddings   AI Search      GPT-4o-mini
    │             │             │
    └──────┬──────┴─────────────┘
           │
           ▼
      Blob Storage


#############################################################################################
############################################ PART 6 #########################################
#############################################################################################

Suggested Learning Roadmap (Next 2 Months)
Week 1 - Metadata + Multi-document ingestion

Week 2 - Hybrid Search

Week 3 - Source citations + conversation history

Week 4 - Key Vault integration

Week 5  - Managed Identity

Week 6 - Application Insights

Week 7 - Jenkins CI/CD

Week 8 - Terraform deployment





