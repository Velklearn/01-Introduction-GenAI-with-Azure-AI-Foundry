# Day 3 — Generative AI with Azure AI Foundry

## Before we start: how Day 3 is organized

Today we build Generative AI applications with **Azure AI Foundry** (recently rebranded **Microsoft Foundry**). Before the first challenge, take two minutes to understand the setup — it explains what you'll see in the portal and why you won't have to create the heavy resources yourself.

### What is Azure AI Foundry?

Azure AI Foundry is Microsoft's unified platform to **build, deploy and manage GenAI applications**: deploy models (GPT, embeddings...), build agents, connect your own data for RAG, and monitor everything in one place. Think of it as the "factory" where all the GenAI pieces come together — models, data, agents, evaluation.

### The shared infrastructure (already created for you)

Everything for Day 3 lives in a single shared resource group, **`day_3`**, in the **Sweden Central** region. Your teacher has already created the resources inside it — open it in the [Azure Portal](https://portal.azure.com) and you'll see them:


- **`foundry-resource-day-3`** — the **Azure AI Foundry resource**. This is the top-level container. The models you'll use (**gpt-5-mini**, **gpt-4.1-mini**, **text-embedding-3-small**) are already deployed here, at the resource level, so everyone shares the same deployments — and the same quota pool.
- **`proj-default`** — a default project. You will create **your own project** inside the Foundry resource (one per student), so your agents, indexes and data stay isolated from everyone else's.
- **`ai-search-day-3`** — a shared **Azure AI Search** service (Basic tier, type *Foundry IQ*). You'll use it for RAG in a later challenge: each of you creates **your own index** inside it (named with your first name, e.g. `orbis-yourname`), so your knowledge base doesn't collide with anyone else's.
- **`ragstorageday3`** — a shared **Azure Blob Storage** account. When you build your RAG index, the documents you upload are stored here before Azure AI Search indexes them.

<figure style="width: 50%">
  <img alt="Shared day_3 resource group with AI Search, Foundry resource and default project" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNWdOQnc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--12eff429d4008766e5f66bb96646786e12617a1c/Capture%20d%E2%80%99e%CC%81cran%202026-06-14%20a%CC%80%2021.20.49.png" />
</figure>

⚠️ **You do not create these resources.** They're shared, already configured, and your teacher will clean them up after the training. Your job is to create **your own project** inside the shared Foundry resource, and (later) **your own index** inside the shared AI Search.

> 🔑 **Why share the resource instead of one each?** Model quota (tokens per minute) is granted *per model, per region, at the subscription level* — a single shared pool for the whole group. Deploying the models once, on one shared resource, means nobody fragments that pool. Each student's *project* consumes the shared deployments without re-deploying anything. This is exactly how a platform team sets things up in a real company: shared expensive infrastructure, isolated workspaces on top.

### Two portals, two jobs

You'll move between two interfaces — know which is which:

- **The Azure Portal** ([portal.azure.com](https://portal.azure.com)) — where you *manage the resource*: see it in the `day_3` resource group, check access (IAM), region, quota, billing. This is the "infrastructure" view.
- **The Foundry Portal** ([ai.azure.com](https://ai.azure.com)) — where you *build*: create your project, deploy/use models, build agents, connect data, run evaluations. This is the "developer" view, and where you'll spend most of Day 3.

### A note on the Foundry UI: Classic for the exercises, New in livecode

Microsoft ships **two portal experiences side by side** at `ai.azure.com` — **Foundry (Classic)** and **Foundry (New)** — switchable via a **toggle in the top banner** (purple = New is ON, grey = Classic). They are not the same tool with a different skin: the new one is a focused redesign for the agentic-AI era.

**For the hands-on exercises, we use the Classic experience** (toggle OFF / grey) — it's stable, complete, and what the screenshots show. Later, your teacher will **demo the New Foundry experience in livecode** so you see where Microsoft is heading (the GA Agent Service, **Foundry IQ** for RAG, the tool catalog). So: follow the exercises in Classic, and just watch the New experience during the livecode. If a screen looks different from a screenshot, first check that your toggle matches (it should be grey/Classic for the exercises).

---

# Challenge 1: Introduction to GenAI with Azure AI Foundry

## Overview

🎯 **Exercise objectives**:

* Introduce participants to Generative AI using the Azure AI Foundry portal.
* Deploy a GenAI model (**gpt-5-mini**) and understand rate limits and quota.
* Build your first python application to interact with the model and experiment with different prompt engineering techniques.

🔧 **Tools**:

* **VS Code** for interactive coding
* **Azure AI Foundry** to deploy and interact with GenAI models
* **GitHub** to host the code of your Apps

---
## 📃 Instructions

In this challenge, you will learn how to use the Azure OpenAI API with python to interact with GenAI models. By the end of this exercise, you will have a better understanding of how to build a simple Chat using GPT-based models with different prompt engineering techniques.

### 1. How the Azure AI Foundry resource was created

⚠️ **You do not need to create this resource: the Teacher already did it for the training.** Just read this first section to know how to do it yourself in the future for another Azure account. The Challenge starts in Section 2.

The Azure AI Foundry resource was created in the shared `day_3` resource group, in the **Sweden Central** region, with the pricing tier **S0**. Why Sweden Central and not France Central? Because of **quota**: Azure OpenAI model quota is granted *per model, per region, at the subscription level*, and on this subscription the gpt-5-mini quota lives in Sweden Central. Choosing the region of an AI resource is not (only) a question of latency or data residency — it's first a question of *where your model quota is*. You'll see this notion again in Section 3.

The creation itself takes a few minutes from the Azure Portal: Marketplace → **Azure AI Foundry** → Create, select the subscription and resource group, give it a name (it becomes the domain of your endpoint), keep Public network access, default values for the other tabs, then Review + Create. The resource provides an **endpoint** and an **API key** — the two secrets you will use from python.

---
### 2. Create your Azure AI Foundry project

⚠️ **The Challenge starts here!!**

- Open [Azure AI Foundry](https://ai.azure.com) and sign in using your provided credentials. Make sure the top-banner toggle is on **Classic** (grey, not purple) for the exercises.

- There are two main spaces to know: the **project studio** and the **management center**. The first time you open AI Foundry, you might land in the default project.

<figure style="width: 50%">
  <img alt="Microsoft Foundry home - shared foundry-resource-day-3" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNGtOQnc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--25cd5e12877a46eea81d08c0bb5f94305b52058a/Capture%20d%E2%80%99e%CC%81cran%202026-06-14%20a%CC%80%2021.03.27.png" />
</figure>

- Click **+ Create new** (or **Create project**) and, when asked, choose the **Microsoft Foundry resource** type (the recommended one).

<figure style="width: 50%">
  <img alt="Create project - choose Microsoft Foundry resource type" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNG9OQnc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--1fc28b8f93f1d10da44ae0a1f3a8b891d94048bb/Capture%20d%E2%80%99e%CC%81cran%202026-06-14%20a%CC%80%2021.04.45.png" />
</figure>

- Give the project a name using your first name, e.g. `yourname-project`. ⚠️ In **Advanced options**, make sure the **Resource group is `day_3`** and the **Region is Sweden Central** so your project lands in the shared Foundry resource. Then **Create**.

<figure style="width: 50%">
  <img alt="Create a project - name and day_3 resource group" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNHNOQnc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--18ba77457fc6695043f32e379d5b46f43a46ead0/Capture%20d%E2%80%99e%CC%81cran%202026-06-14%20a%CC%80%2021.06.04.png" />
</figure>

- After the project is created, you land on the **project overview**. Here you can see the **API key** and the **endpoint url** (Microsoft Foundry project endpoint) — we'll need both to build our app.

<figure style="width: 50%">
  <img alt="Project overview - endpoints and API key" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNHdOQnc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--2c8df2e3a241d7a8c0c023b132e8b343a41dd00e/Capture%20d%E2%80%99e%CC%81cran%202026-06-14%20a%CC%80%2021.07.17.png" />
</figure>

---
### 3. Deploy a Model in your project

- In your project, open the **Model catalog** on the left menu.

<figure style="width: 50%">
  <img alt="Model catalog in the project" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNDROQnc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--d465176e3d0fea76e472f39d8e28cb1fef0dab9a/Capture%20d%E2%80%99e%CC%81cran%202026-06-14%20a%CC%80%2021.07.11.png" />
</figure>

- Search for the **`gpt-5-mini`** model and select it. On the model card you can find its information: training cutoff, supported data types (note: **text + image input** — useful later for the multimodal challenge), retirement date, benchmarks. Click **Use this Model**.

<figure style="width: 50%">
  <img alt="gpt-5-mini model card - text and image input, retirement Feb 2027" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNUFOQnc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--073c1deac300ddb8aa3c972c4d1d41fc256038e9/Capture%20d%E2%80%99e%CC%81cran%202026-06-14%20a%CC%80%2021.07.34.png" />
</figure>

- Configure the deployment:
  - **Deployment name**: keep it simple, you will type it in your code — e.g. `gpt-5-mini-yourname`.
  - **Deployment type**: Global Standard (default).
  - **Model version**: default (`2025-08-07`).
  - Open **Deployment details** and set the **Tokens per Minute Rate Limit to 10K**. ⚠️ Do not take more!

  🧠 **Why 10K, and why does it matter?** All deployments of a model in a region share a **single quota pool** at the subscription level. The pool for gpt-5-mini here is 500K TPM — for the whole group. Your deployment *reserves* its rate limit from that pool: if one person takes 200K "just in case", others can't deploy anymore (`InsufficientQuota` error). 10K is far more than this exercise needs, and 11 × 10K leaves plenty of margin. Sizing rate limits to the actual need instead of the maximum is exactly how it works in a real company subscription.

  🛠️ If you get an **InsufficientQuota** error when deploying: don't retry with a bigger number 😄 — raise your hand, a TA will check the pool.

<figure style="width: 50%">
  <img alt="Deploy gpt-5-mini - set Tokens per Minute Rate Limit" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNUlOQnc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--290e45750f2619c33788b6fa9d6332d89f837238/Capture%20d%E2%80%99e%CC%81cran%202026-06-14%20a%CC%80%2021.07.56.png" />
</figure>

- Deploy the model. Then go to **My assets > Models + endpoints** in the left menu and click on your deployment: you will see the **Target URI** (endpoint) and the **API key**. We need them for the app.

<figure style="width: 50%">
  <img alt="Deployment details - Target URI and key" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNU1OQnc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--1fd006f88dc4bff6d6d81dbc92c7f9110119b1bd/Capture%20d%E2%80%99e%CC%81cran%202026-06-14%20a%CC%80%2021.08.32.png" />
</figure>

  💡 **One thing to know about gpt-5-mini**: it is a *reasoning* model — it "thinks" before answering. Expect a couple of seconds of latency before the response: it's not a bug, it's the model working.

---
### 4. Build your first python App to interact with gpt-5-mini

- Create a new project directory next to your other projects. Use a unique name without spaces:

  ```bash
  cd Documents/GitHub
  mkdir myfirstazureapp
  cd myfirstazureapp
  ```

- Open VS Code using the `azure-env` environment, go to the new folder and create a file **`.env`** with the key and endpoint of your deployment:

  ```text
  AZURE_OPENAI_API_KEY="your_key"
  AZURE_OPENAI_ENDPOINT="your_endpoint"
  ```

- ⚠️ **Before anything else, create a `.gitignore` file containing**:

  ```text
  .env
  __pycache__
  .DS_Store
  ```

  🧠 **Why first?** Your `.env` contains a live API key. If you commit it and push to GitHub, your key is public: anyone can use it (and burn the quota — or the budget — of the whole subscription). Leaked keys are one of the most common real-world security incidents with GenAI apps. The `.gitignore` guarantees git never picks it up. **Never commit secrets.**

- Create a new Python file named `app.py` and copy the following code:

  ```python
  # Import main libraries
  import os
  from dotenv import load_dotenv
  from openai import AzureOpenAI

  # loading variables from .env file
  load_dotenv()

  # Authenticate the client using your key and endpoint
  client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-12-01-preview"
  )

  # Interact with your gpt-5-mini deployment
  response = client.chat.completions.create(
      model="gpt-5-mini-yourname", # model = your deployment name!
      messages=[
          {"role": "system", "content": "You are a helpful assistant. Answer like a pirate."},
          {"role": "user", "content": "Who were the founders of Microsoft?"}
      ]
  )

  print(response.choices[0].message.content)
  ```

  > ⚠️ `model=` takes **the name of YOUR deployment** (what you typed in Section 3), not the generic model name.

- Open the Anaconda Prompt with the `azure-env` environment and run:

  ```bash
  python app.py
  ```

You should obtain something like:

  ```
  Ahoy, matey! The founders of Microsoft be Bill Gates and Paul Allen, savvy?
  ```

- If you want to see the whole answer in json format, add this to `app.py`:

  ```python
  print(response.model_dump_json(indent=2))
  ```

  🧠 Look at the `usage` section in the json: prompt tokens, completion tokens... and reasoning tokens! This is what you pay for, and what your 10K TPM rate limit counts.

---
### 5. Play with different Prompt techniques

Let's try different prompt techniques. For each technique, take notes about the style and the impact on the answer.

- **Prompt using instructions:**

  ```python
  response = client.chat.completions.create(
      model="gpt-5-mini-yourname", # your deployment name
      messages=[
          {"role": "system", "content": """Assistant is an intelligent chatbot designed to help users answer their tax related questions.
          Instructions:
          - Only answer questions related to taxes.
          - If you're unsure of an answer, you can say I don't know or I'm not sure and recommend users go to the IRS website for more information. """},
          {"role": "user", "content": "When are my taxes due?"}
      ]
  )
  ```

- **Prompt using context:**

  ```python
  response = client.chat.completions.create(
      model="gpt-5-mini-yourname", # your deployment name
      messages=[
          {"role": "system", "content": """Assistant is an intelligent chatbot designed to help users answer technical questions about Santa Claus. Only answer questions using the context below and if you're not sure of an answer, you can say 'I don't know'.

          Context:
          - Santa Claus has two sons: Peter and Jack."""},
          {"role": "user", "content": "What is the name of the third Santa's son?"}
      ]
  )
  ```

- **Prompt using Few-shot learning:**

  ```python
  response = client.chat.completions.create(
      model="gpt-5-mini-yourname", # your deployment name
      messages=[
          {"role": "system", "content": "Assistant is an intelligent chatbot designed to answer users"},
          {"role": "user", "content": "This is awesome!  "},
          {"role": "assistant", "content": "Positive "},
          {"role": "user", "content": "This is bad!"},
          {"role": "assistant", "content": "Negative"},
          {"role": "user", "content": "Wow that movie was rad!"},
          {"role": "assistant", "content": "Positive"},
          {"role": "user", "content": "The movie was terrific"},
      ]
  )
  ```

- **Prompt for non-chat scenarios:**

  ```python
  response = client.chat.completions.create(
      model="gpt-5-mini-yourname", # your deployment name
      messages=[
          {"role": "system", "content": """You are an assistant designed to extract entities from text. Users will paste in a string of text and you will respond with entities you've extracted from the text as a JSON object. Here's an example of your output format:
          'name': '',
          'company': '',
          'phone_number': ''
          """},
          {"role": "user", "content": """Hello. My name is Robert Smith. I'm calling from Contoso Insurance, Delaware. My colleague mentioned that you are interested in learning about our comprehensive benefits policy. Could you give me a call back at (555) 346-9322 when you get a chance so we can go over the benefits?"""}
      ]
  )
  ```

- **Build a Chat loop** (after creating the client, try the following — use `Ctrl + C` to stop the loop):

  ```python
  conversation=[{"role": "system", "content": "You are a helpful assistant."}]

  while True:
      user_input = input("Q:")
      conversation.append({"role": "user", "content": user_input})

      response = client.chat.completions.create(
          model="gpt-5-mini-yourname", # your deployment name
          messages=conversation
      )

      conversation.append({"role": "assistant", "content": response.choices[0].message.content})
      print("\n" + response.choices[0].message.content + "\n")
  ```

Note that these models are optimized to work with inputs formatted as a conversation. The `messages` variable passes an array of dictionaries with different roles delineated by `system`, `user`, and `assistant`. The system message primes the model with context or instructions on how it should respond — this is why building good prompt templates matters to get the best possible answers.

🧠 Notice in the chat loop that **the model has no memory**: we re-send the whole `conversation` list at every turn. The "memory" of a chatbot is just the conversation history you keep appending — and it counts in your tokens.

---
### 6. Bonus: Compare two models on the same prompts

Go back to the Model catalog and deploy a **second model**: `gpt-4.1-mini` (a *non-reasoning* model — same deployment steps, **TPM 10K**, its quota pool is separate from gpt-5-mini's). Then re-run the prompts of Section 5, changing only the `model=` deployment name.

Compare: response latency (reasoning vs non-reasoning), style and quality of the answers, and the `usage` token counts in the json. When would you pick each model in a real application — and what does that mean for cost?

---

Congratulations! You have built your first GenAI App with Azure AI Foundry. 🎉

### Don't forget to save your work!

Save your files: File > Save. Then, close all the tabs in your browser and VS Code windows. You can safely close the Anaconda Prompt (or Terminal).

💡 Don't forget to **push your code to GitHub** — and double-check that **`.env` is NOT in the pushed files** (it shouldn't be, thanks to your `.gitignore`).

1. Open GitHub Desktop.
2. It should automatically detect any file with modifications. If not, ask a TA.
3. Make sure these files are ticked (and `.env` is not there!), and write a _commit message_ in the bottom left form.
4. Click on the "Commit to `master`" button at the bottom of the form.
5. Click on the "Push `origin`" button at the top of the window.

---
## 🥇 Key learning points

By the end of this exercise, you will have:

* Understood the Day 3 architecture: a shared Foundry resource, one project per student, shared AI Search.
* Deployed a GenAI model in Azure AI Foundry and understood how **quota pools and rate limits** are shared across a subscription.
* Built python apps to interact with GenAI models using different prompt engineering techniques.
* Handled API **secrets properly** with a `.env` file kept out of git.

That's it! Take a small break before diving into the next exercise.