# What is DefaultAzureCredential()

DefaultAzureCredential is not a credential itself. It's a credential chain.

Think of it as:

    credential = DefaultAzureCredential()

which conceptually behaves like:

try:
    EnvironmentCredential()
except:
    try:
        WorkloadIdentityCredential()
    except:
        try:
            ManagedIdentityCredential()
        except:
            try:
                AzureCliCredential()
            ...

It tries multiple authentication methods in order until one successfully obtains an access token.

# Typical order (Python SDK)

The exact order depends on the Azure Identity library version and configuration, but for recent versions it's approximately:

DefaultAzureCredential
│
├── EnvironmentCredential
├── WorkloadIdentityCredential
├── ManagedIdentityCredential
├── SharedTokenCacheCredential (Windows)
├── AzureCliCredential
├── AzurePowerShellCredential
├── AzureDeveloperCliCredential
└── InteractiveBrowserCredential (disabled by default)


# AzureCliCredential()

So locally you bypass DefaultAzureCredential entirely.

Authentication flow:

    Azure CLI
         │
    az login
         │
    Access Token
         │
    Key Vault

No managed identity is involved.

# A helpful mental model

Think of DefaultAzureCredential as an authentication strategy chain:

                    DefaultAzureCredential
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
 Environment        Workload Identity      Managed Identity
 Credential              Credential             Credential
        │                     │                     │
        └────────── First one that succeeds ───────┘
                              │
                              ▼
                   Access Token (JWT)
                              │
                              ▼
                         Azure Key Vault
 
This design lets your application use the most appropriate authentication mechanism for its environment while keeping your application code unchanged.


They don't authenticate with portal.azure.com.
They authenticate with Microsoft Entra ID (Azure AD), which is Azure's identity service.

The Azure portal is just a web application that itself uses Microsoft Entra ID.

####################################
######### The big picture ##########
####################################

Every Azure SDK client eventually needs an OAuth 2.0 access token.

Conceptually:

    Your Application
           │
           ▼
    DefaultAzureCredential
           │
           ▼
    Chooses an authentication strategy
           │
           ▼
    Microsoft Entra ID (directly or indirectly)
           │
           ▼
    Access Token (JWT)
           │
           ▼
    Azure Key Vault

The only difference between the strategies is how they prove their identity to Microsoft Entra ID.

# Example 1: Service Principal

You have:

    Client ID
    Client Secret
    Tenant ID

The SDK sends something like:

    POST https://login.microsoftonline.com/<tenant>/oauth2/v2.0/token

    client_id=...
    client_secret=...
    grant_type=client_credentials
    scope=https://vault.azure.net/.default

    Entra ID validates the secret.
    
    ↓
    
    Returns JWT access token.

# Example 2: Azure CLI

You already executed

    az login

The Azure CLI has already authenticated with Entra ID and cached tokens.

When the SDK asks:

    AzureCliCredential()

it simply asks Azure CLI:

    "Give me an access token for Key Vault."
    
    Azure CLI refreshes the token if necessary.

# Example 3: Managed Identity
# Example 4: Workload Identity

# So who issues the token?

Always: Microsoft Entra ID

The strategies only differ in how they authenticate themselves.

# Then what does Key Vault do?

When your SDK calls Key Vault:

GET https://abindevlabs-kv.vault.azure.net/secrets/...
Authorization: Bearer <JWT>

Key Vault:
    Validates the JWT.
    Determines which identity it represents.
    Checks Azure RBAC (or access policies, depending on the vault configuration).
    Returns the secret or a 403 Forbidden.

# A small but important terminology correction

Instead of saying:

    "It reaches portal.azure.com"

it's more accurate to say:

    "It reaches Microsoft Entra ID's OAuth 2.0 token endpoint (either directly or through Azure infrastructure) to obtain an access token."

    That's the identity service. The Azure portal is just one client application that also authenticates against Microsoft Entra ID.