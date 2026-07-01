1. Project Evaluation
2. Managed Identity
3. Complete Architecture
4. Code Changes
5. Create AKS
6. Add role assignments
7. Role Based Access Control


#########################################################
################## 1. Project Evolution: ###################
#########################################################

main
│
├── 1. Kubernetes Secrets
│
├── 2. key_vault_integration
│      ├── Service Principal
│      └── Azure Key Vault
│
**├── 3. managed_identity
│      ├── AKS Managed Identity
│      ├── Azure Key Vault
│      └── ConfigMap**
│
└── 4. workload_identity
       ├── AKS Workload Identity
       ├── Azure Key Vault
       └── ConfigMap

# Stage 1 - Kubernetes Secrets (Already completed)

    Pod
     │
     ▼
    Kubernetes Secret
     │
     ├── OpenAI Key
     ├── Search Key
     └── Storage Key

    Cons:
    Kubernetes admins can read secrets

# Stage 2 - Service Principal + Key Vault 

    Pod
     │
     ▼
    Client Secret (SP)
     │
     ▼
    Azure Key Vault
     │
     ├── OpenAI Key
     ├── Search Key
     └── Storage Key

    Cons
    You still have: Client Secret inside Kubernetes.

# Stage 3 - AKS Managed Identity

Azure thought:

"Why should customers create Service Principals?"

So Azure introduced Managed Identity.

    AKS Cluster
          │
    Managed Identity
          │
          ▼
    Azure Key Vault
          │
          ├── Foundry Key
          ├── Search Key
          └── Storage Key

Pros

    ✔ No client secret
    
    ✔ Azure rotates credentials
    
    ✔ More secure
    
Cons
    
    Permissions are granted to the entire AKS cluster.

    Every pod can potentially use that identity.

# Stage 4 - AKS Workload Identity

Microsoft then realized:

"Why should the whole cluster share one identity?"

Instead: Every application has its own Azure identity.

Architecture:

    Pod
     │
     ▼
    Service Account
     │
     ▼
    Federated Credential
     │
     ▼
    User Assigned Managed Identity
     │
     ▼
    Key Vault

Benefits:
Each application has

    separate permissions
    least privilege
    independent identities

Exactly what enterprise security teams want.

| Feature                   | Kubernetes Secret | Service Principal | Managed Identity | Workload Identity |
| ------------------------- | ----------------- | ----------------- | ---------------- | ----------------- |
| API keys in Kubernetes    | Yes               | No                | No               | No                |
| Client Secret             | No                | Yes               | No               | No                |
| Azure manages credentials | No                | No                | Yes              | Yes               |
| Pod-level identity        | No                | No                | No               | Yes               |
| Enterprise Ready          | Medium            | Good              | Very Good        | Excellent         |
| Microsoft Recommendation  | No                | Legacy            | Good             | **Best**          |

################################################################
##################### 2. MANAGED IDENTITY ######################
################################################################

# Do we link AKS cluster with azure key vault?

No, you don't directly "link" AKS to Key Vault.

Instead, you give an Azure identity to the AKS cluster (or pods), and then authorize that identity to access Key Vault.

Think of it like this:

Today (Service Principal)

    AKS Pod
       │
    Client ID + Client Secret
       │
    Authenticate
       │
    Azure Key Vault

With Managed Identity:

    AKS Pod
       │
    Managed Identity
       │
    Authenticate
       │
    Azure Key Vault

The identity changes, but Key Vault is still the central place where your secrets live.

# What Changes in Azure?

# Step 1. Enable Managed Identity on AKS
A. System Assigned Managed Identity (most common)

    AKS
        ↓
    Settings
        ↓
    Identity

B. User Assigned Managed Identity

    You explicitly create an identity:
    
    Managed Identity
         ↓
    Assign to AKS
    
    Useful when multiple services share the same identity.
    
    For learning, System Assigned is enough.

# Step 2. Get the Identity

Once enabled, Azure creates something like:

    AKS Cluster
    
    Identity
    
    Principal ID
    xxxxxxxxxxxxxxxx
    
    Object ID
    xxxxxxxxxxxxxxxx

Think of this as: Azure User except it's for your AKS cluster.

# Step 3. Give the Identity Access to Key Vault

Go to:

    Azure Key Vault
            ↓
    Access Control (IAM)
            ↓
    Add Role Assignment

Role:

    Key Vault Secrets User

Member:

    AKS Managed Identity

That's the critical step.

You're telling Azure: "This AKS cluster is allowed to read secrets."

# What Actually Happens?

    Before:
    
        Pod
        
        ↓
        
        Client Secret
        
        ↓
        
        Key Vault

    After:
    
        Pod
        
        ↓
        
        Managed Identity
        
        ↓
        
        Azure AD
        
        ↓
        
        Key Vault
        
        Azure AD verifies the identity automatically.

# Step 4. Application Code

Before:

credential = ClientSecretCredential(
    tenant_id=...,
    client_id=...,
    client_secret=...
)

After:

credential = DefaultAzureCredential()

Nothing else changes.

# Step 5. Deployment Changes
Remove client id, secret, tenant id

# Step 6. Key Vault Doesn't Change

Nothing changes there.

The only difference is who is asking for the secrets.

Old:
    Service Principal

New:
    Managed Identity

###########################################################
################ 3. Complete Architecture #################
###########################################################

                Azure Subscription

 ┌──────────────────────────────────────────────┐
 │                                              │
 │        Azure Kubernetes Service              │
 │                                              │
 │    ┌────────────────────────────┐            │
 │    │ FastAPI Pod                │            │
 │    │                            │            │
 │    │ DefaultAzureCredential()   │            │
 │    └─────────────┬──────────────┘            │
 │                  │                           │
 │                  ▼                           │
 │        System Assigned Managed Identity      │
 │                                              │
 └──────────────────┼───────────────────────────┘
                    │
                    │ Azure AD Authentication
                    ▼
          Azure Key Vault
      ┌──────────────────────┐
      │ foundry-api-key      │
      │ search-api-key       │
      │ storage-connection   │
      └─────────┬────────────┘
                │
                ▼
        Azure AI Foundry
        Azure AI Search
        Blob Storage
 
# Is There a "Link" Between AKS and Key Vault?

Not in the sense of creating a connection between the two resources.

Instead, Azure uses Role-Based Access Control (RBAC):

1. AKS has an identity.
2. Key Vault has permissions.
3. You assign the AKS identity the Key Vault Secrets User role.

That's the "link."

###################################################
############## 4. Code Changes ####################
###################################################

keyvault.py
    if environment == "local":
        return AzureCliCredential()

    return DefaultAzureCredential()

created configmap.yaml

Updated deployment.yaml
        env:

        - name: AZURE_FOUNDRY_ENDPOINT
          valueFrom:
            secretKeyRef:
              name: rag-config
              key: AZURE_FOUNDRY_ENDPOINT

##############################
###### 5. Create AKS #########
##############################

#  Use Azure CLI to get the principal id

az aks show --resource-group abindev-rg --name aks-practice-cluster --query identity

{
  "delegatedResources": null,
  "principalId": "b1d0e89a-bbdb-45d7-86d4-b3a264c6e308",
  "tenantId": "f8cea540-60d7-4415-93b2-6dd05ecad6c0",
  "type": "SystemAssigned",
  "userAssignedIdentities": null
}

# Go to key vault
    Access Control (IAM)

        ↓

    Add Role Assignment
    for : aks-practice-cluster-agentpool / aks-practice-cluster or 
    Role : Key Vault Secrets User
    type: user assigned managed identity

    Assign it to : AKS Cluster using its Principal ID.

# Important Points:
    AKS control plane uses system managed identity
    AKS node pool uses user assigned managed identity
    Both are created automatically in AKS
    Create role assignments for aks-practice-cluster-agentpool in Azure KV.

# System Managed Identity:

Why didn't the system-assigned identity work?

    Your cluster has:
    
    System Assigned Managed Identity
            │
            ▼
    aks-practice-cluster

This identity is primarily used by the AKS control plane to manage Azure resources on behalf of the cluster, such as:

    Creating load balancers
    Managing public IPs
    Managing disks
    Interacting with Azure infrastructure

Your application inside the pod was not using this identity.

# What is the kubelet identity?

AKS also creates another managed identity:

    aks-practice-cluster-agentpool

    This identity is attached to the node pool.

Its primary job is things like:

    Pulling images from ACR
    Accessing Azure resources on behalf of the node
    Being available through the Instance Metadata Service (IMDS)

Since your pods are running on those nodes, DefaultAzureCredential() discovered that managed identity and used it.

# Is agentpool one node?

AKS Cluster
│
├── Control Plane
│      │
│      └── System Assigned MI
│
└── Node Pool (agentpool)
       │
       ├── Node 1
       ├── Node 2
       └── Node 3

The managed identity belongs to the node pool, not to an individual node.

Every VM in that node pool uses that same managed identity.

# System-assigned vs User-assigned Managed Identity

# 1. System-assigned
    
    Created automatically for one Azure resource.

    AKS Cluster
          │
          ▼
    System Assigned MI

Characteristics:

    Tied to one resource
    Deleted automatically when the resource is deleted
    Cannot be shared

# 2. User-assigned

A standalone Azure resource.

User Assigned MI
        │
        ├── VM
        ├── App Service
        ├── AKS
        └── Function App

Characteristics:

    Exists independently
    Can be attached to multiple Azure resources
    Survives even if one resource is deleted

Your kubelet identity is a user-assigned managed identity that AKS created automatically.

#######################################################
############# 7. Role Based Access Control ############
#######################################################

# 1. When we assign the role for these identities in Azure Key vault (IAM), 
what does this process called generally in azure?
    
In Azure, this process is generally called authorization using Azure RBAC (Role-Based Access Control).

Authentication answers: Who are you?
Authorization answers: What are you allowed to do?

# In your AKS scenario, the flow is:

    AKS Pod
       │
       ▼
    DefaultAzureCredential()
       │
       ▼
    Managed Identity Authentication
       │
       ▼
    Microsoft Entra ID issues an access token
       │
       ▼
    Azure Key Vault receives the token
       │
       ▼
    Azure RBAC Authorization
       │
       ▼
    Checks:
    "Does this identity have 'Key Vault Secrets User' on this vault?"

So when you go to Key Vault → Access Control (IAM) → Add role assignment, 
you're performing an Azure RBAC role assignment. This is an authorization step.


# The three core concepts

Every Azure RBAC role assignment consists of:

# 1. Security Principal (Who?)

    User
    Group
    Service Principal
    Managed Identity

In your case: aks-practice-cluster-agentpool

# 2. Role Definition (What can they do?)

    Examples:
        Reader
        Contributor
        Owner
        Key Vault Secrets User
        Key Vault Administrator
        Storage Blob Data Reader

# 3. Scope (Where?)

Permissions can be granted at different levels:

Management Group
     │
Subscription
     │
Resource Group
     │
Resource

# A good way to explain

If asked, "How did you allow your AKS application to access Key Vault?", you could say:

"The application authenticates using a managed identity through DefaultAzureCredential. 
I then authorized that managed identity by creating an Azure RBAC role assignment, 
granting it the Key Vault Secrets User role scoped to the Azure Key Vault. 
This follows the principle of least privilege, allowing the application to read secrets 
without storing credentials in the application."