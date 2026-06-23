Complete Azure RAG Architecture

By the end of Milestone 1, your architecture will look like this:

                    Azure AI Foundry
                           │
          ┌────────────────┼────────────────┐
          │                                 │
    gpt-4o-mini                  text-embedding-3-small
          │                                 │
          └────────────────┬────────────────┘
                           │
                       FastAPI
                           │
          ┌────────────────┼────────────────┐
          │                                 │
 Azure Blob Storage              Azure AI Search
          │                                 │
       PDF Files                  Vector Index

####################### 
# 1. Azure AI Foundry #
#######################

What credentials do you need?

# Endpoint

Use:

https://YOUR_RESOURCE.services.ai.azure.com/openai/v1

# API Key

    Copy from:
    
    AI Foundry
        ↓
    Management Center
        ↓
    Keys

############################
# 2. Azure Storage Account #
############################

# Create

    Create Resource
          ↓
    Storage Account

# After creation

# Open

    Storage Account
         ↓
    Access Keys

You need:

# Storage Account Name

Example:

    abinragstorage
Store: AZURE_STORAGE_ACCOUNT_NAME=abinragstorage

# Access Key

Copy: Key1

Store: AZURE_STORAGE_ACCOUNT_KEY=

# Connection String

Same page: Connection String

Copy:

    Example:
    DefaultEndpointsProtocol=https;
    AccountName=abinragstorage;
    AccountKey=xxxxxxxx;
    EndpointSuffix=core.windows.net

Store: AZURE_STORAGE_CONNECTION_STRING=
    
    This is what we'll use.

##################
## Blob Container
##################

Create:

    Storage Account
          ↓
    Containers
          ↓
    + Container

Name: documents
Store: AZURE_STORAGE_CONTAINER=documents

###################
# Azure AI Search #
###################

This will become our Vector Database.

# Create

    Go to Portal

    Azure AI Search
          ↓
    Create

    Recommended:
    Setting	    Value
    Pricing	    Basic
    Region	    South India
    Resource Group	rg-rag-demo

# Search Endpoint
    After creation --> Open

    Azure AI Search
          ↓
    Overview

Copy: Search Endpoint
Example: https://abinsearch.search.windows.net
Store: AZURE_SEARCH_ENDPOINT=

# Admin Key

    Go to
    
    Azure AI Search
          ↓
    Settings
          ↓
    Keys

Copy: Primary Admin Key

Store: AZURE_SEARCH_API_KEY=

# Index Name

We will create later.

Use: AZURE_SEARCH_INDEX_NAME=documents


        

