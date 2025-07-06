import os
from fileinput import filename
from importlib.metadata import metadata
from itertools import count

from github import Github
import chromadb
import openai
import httpx
import uuid
from chromadb.utils import embedding_functions
from posthog import api_key

github_access_token=""

g = Github(f"{github_access_token}")

repo_owner = 'torvalds'
repo_name = 'linux'

repo = g.get_repo(f"{repo_owner}/{repo_name}")
Changed_Files =[]
Pull_Requests = []

count = 0

for pull_request in repo.get_pulls(state='closed'):
    print(f"Checking Pull Request #{pull_request.number} - {pull_request.title}")

    files = pull_request.get_files()
    sFiles = ""

    for file in files:
        #print(f"Checking File : {file.filename}")
        sFiles = sFiles + "," + file.filename
        #print("\n" + "=" * 50 + "\n")
    Changed_Files += [sFiles]
    Pull_Requests += [pull_request.number]
    count += 1
    print("\n" + "=" * 50 + "\n")
    if count > 10:
        break
#print(Changed_Files)
print(Pull_Requests)

CHROMA_DATA_PATH = "chroma_data"
EMBED_MODEL = "all-mpnet-base-v2"
COLLECTION_NAME = str(uuid.uuid4())

client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)

collection = client.create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_func,
    metadata={"hnsw:space": "cosine"}
)

collection.add(
    documents=Changed_Files,
    ids=[f"id{i}" for i in range(len(Changed_Files))],
    metadatas=[{"genre":g} for g in Pull_Requests]
)


pull_request1 = repo.get_pull(896)
files1 = pull_request1.get_files()
filenames = ""
for file in files1:
    filenames += file.filename + ","

def text_embedding(text):
    # Call the embeddings endpoint

    client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

    response = client.embeddings.create(
        model="text-embedding-ada-002",  # Efficient and widely used model
        input=text
    )
    return response.data[0].embedding[:768]

vecor = text_embedding(filenames)

query_results = collection.query(
    query_embeddings=vecor,
    n_results=1
)

print(query_results.keys())
print(query_results.values())
print(query_results["documents"])
print(query_results["ids"])
print(query_results["distances"])
print(query_results["metadatas"])

metadata = query_results["metadatas"]
List_PR_number = metadata.pop(0)
PR_numbers = List_PR_number[0]
PR_number = PR_numbers.get("genre")

####
print(query_results["documents"])

print(query_results["ids"])

print(query_results["distances"])

print(query_results["metadatas"])

metadata = query_results["metadatas"]
List_PR_number = metadata.pop(0)
PR_numbers = List_PR_number[0]
PR_number = PR_numbers.get("genre")

pull_request2 = repo.get_pull(PR_number)
files = pull_request2.get_files()

def get_File_Changes(files):  # 2 usages
    FINAL_PR=""
    for file in files:
        patch_content= file.patch

    if patch_content is not None:
        patch_lines=patch_content.split('\n')

    patch_lines_before=patch_lines
    patch_lines_after=patch_lines

    added_lines = [line for line in patch_lines if line.startswith('++') and not line.startswith('+++')]
    removed_lines = [line for line in patch_lines if line.startswith('--') and not line.startswith('---')]

    # Identify and print added lines
    added_lines_print = [line[1:] for line in patch_lines if line.startswith('++') and not line.startswith('+++')]
    # Add similar function for removed lines
    removed_lines_print = [line[1:] for line in patch_lines if line.startswith('--') and not line.startswith('---')]

    print("Added Lines:")
    for added_line in added_lines_print:
        print(added_line)

        print("Removed Lines:")
        for removed_line in removed_lines_print:
            print(removed_line)

        for added_line in added_lines:
            if patch_lines_before is not None:
                patch_lines_before = patch_lines_before.remove(added_line)

        for removed_line in removed_lines:
            if patch_lines_after is not None:
                patch_lines_after = patch_lines_after.remove(removed_line)

    if patch_lines_after is not None:
        patch_lines_after = patch_lines_after.remove(removed_line)

    print("Before:")
    print(patch_lines_before)
    Before_PR = ""
    if patch_lines_before is not None:
        # Before_PR = Before_PR.join([str(item) for item in patch_lines_before])
        Before_PR = Before_PR.join(patch_lines_before)

    print("After:")
    print(patch_lines_after)
    After_PR = ""
    if patch_lines_after is not None:
        After_PR = After_PR.join(patch_lines_after)

    if len(Before_PR) > 0 or len(After_PR) > 0:
        FINAL_PR = FINAL_PR + "Before Pull Request: " + Before_PR + " After Pull Request: " + After_PR + "\n"

    return FINAL_PR

Final_PR2 = get_File_Changes(files)
Final_PR1 = get_File_Changes(files1)

res = "\n".join(str(item) for item in query_results['documents'][0])

prompt = f'Based on the content in {Final_PR2 + Final_PR1}, please suggest the changes in ' + Final_PR1

messages = [
    {"role": "system", "content": "You answer questions about Pull Requests."},
    {"role": "user", "content": prompt}
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # Corrected model name for OpenAI
    messages=messages,
    temperature=0
)

response_message = response.choices[0].message.content

print(response_message)





