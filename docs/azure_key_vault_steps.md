
Phase 1: Key Vault + API Keys (easier, good learning)

Phase 2: Managed Identity + Key Vault (enterprise)

Phase 3: Managed Identity for Foundry/Search/Storage (advanced)

#########################################
################ Phase 1 ################
#########################################

# Step 1: Create Azure Key Vault
    Key Vault Name : abinlabs-kv

# Step 2: Add Secrets
    Go:
    
    Key Vault
       ↓
    Objects
       ↓
    Secrets
       ↓
    Generate / Import

-- handle error

    Assign the correct role
    
    If you're an administrator:
    
    Key Vault
        Access control (IAM)
        Add role assignment
    Assign:
        Key Vault Secrets Officer (for secrets)
        Key Vault Administrator (full vault data access)
        Select your user/service principal
    Save
    
    Wait 5–15 minutes for propagation.

# Step 3: Install SDK
    pip install azure-keyvault-secrets
    pip install azure-identity
Add the above library in the requirements.txt

# Step 4: Add Key Vault URL
Go:
    Key Vault
        ↓
    Overview

Copy:
    https://abinlabs-kv.vault.azure.net/

Add to: .env
KEY_VAULT_URL=https://abinlabs-kv.vault.azure.net/

# Step 5: Create config/keyvault.py

# Step 6: Create Central Settings File

# Step 7: What code changes required?
    Files To Modify
    -- embedding_service.py
    -- chat_service.py
    -- search_service.py
    -- blob_service.py

# Step 8: Local Testing
# Step 9: Grant Yourself Access

    Go:
    
    Key Vault
       ↓
    Access Control (IAM)
    
    Add role:
    
    Key Vault Secrets User
    
    Assign to:
    
    Your Azure User
    
    Otherwise local testing will fail.
# Step 10: AKS Later

######################################
######### Before Deployment ##########
######################################
# step 1. create SP
    az ad sp create-for-rbac --name rag-keyvault-sp

# Step 2: Grant Key Vault Access
    Go:
        Key Vault
          ↓
        Access Control (IAM)
          ↓
        Add Role Assignment