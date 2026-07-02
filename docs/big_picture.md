
# Problem statement is to develop and deploy a RAG based architecture to answer queries 
# on Resume in the Azure Platform

#############################
######## Development ########
#############################

## 001. Azure Services

# 1. Create a resource group
# 2. Create a storage account service (Store PDF document)
# 3. Create a azure open AI service (deploy GPT model and text embedding model)
# 4. Create a azure AI search service (indexing, upload documents, vector search)

## 002. Create Project Code

# 1. Create blob storage service (Access, Upload, Download PDF in the storage)
# 2. Create PDF service (load, read pages, Consolidated text)
# 3. Create Chunk Service (convert text to list of chunks)
# 4. Create chat model service (Access, call GPT, get prediction)
# 5. Create embedding model service (Access, call model, convert text to vector)
# 6. Create RAG Service (Import embedding, PDF, Chunk, Chat service,
#    convert question, does vector search, answer user question using chat model)
# 7. Create Ingestion Service (load PDF, convert to chunks, create indexing, 
#   upload documents to azure AI search)

## 003. Store Credentials (.env)

# 1. AZURE OPEN AI API KEY and URL, model name
# 2. Storage Account Connection String, container name
# 3. AZURE AI SEARCH API KEY and URL, index name
# 4. CHUNK SIZE, OVERLAP

## 004. Create FastAPI

# 1. Create all the service as separate py file
# 2. Create main.py file (uvicorn startup)


#############################
######## Deployment #########
#############################

## 001. Create Docker Image

# 1. Create Dockerfile (app folder, requirements.txt, python slim, command)
# 2. Create Docker image
# 3. Tag Docker image to ACR
# 4. Push Docker image to ACR

## 002. Create AKS Cluster service in Azure Portal

# 1. Attach AKS cluster to ACR container

## 003. Create ACR service

## 004. Create deployment,service, rag secrets manifest files

# 1. Define spec, container name, port, image reference, env reference

###############################################################################################
# Note: All the keys, configuration are exposed via kubernetes secrets which admin can access #
###############################################################################################

##################################
######## Enhancement -01 #########
##################################

## 001. Azure Key Vault Integration

# 1. Create Azure Key Vault service (AKV)

# 2. Add role assignment (secrets user, administrator) for the user (Your self)

# Note: Azure CLI credential works in local using DefaultAzureCredential chain, but not inside the container

# 3. Create Service Principal to authenticate AKV

# 4. Add role assignment for the created service principal in AKV (secrets user)

# 5. Update the code to use SecretClientCredential to authenticate + authorization

###############################################################################################
# Note: with KV, secret exposed has reduced, but still we are exposing service principal id's #
###############################################################################################

##################################
######## Enhancement -02 #########
##################################

## 001. Managed Identity Integration + ConfigMap

# 1. system assigned (Cluster Identity) and user assigned identities (Kubelet Identity) are automatic while creating AKS Cluster

# 2. Create role assignment in AKV, select managed identity, 
#    pick aks-cluster-agent-pool (assign secret user role)
# 3. To maintain best practices, create ConfigMap and move all the configuration values here

########################################################################################################################################
# Note: DefaultAzureCredential works in local and production, but for ease purpose use AzureCLICredential in local to authenticate AKS #
########################################################################################################################################