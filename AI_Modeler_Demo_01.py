import os
from git import Repo
import shutil
import requests

# --- Configuration ---
repo_dir = "repos"
file_to_push = "AI_Modeler_Demo_01.py"
branch = "main"
username = "user01"

# Get GitHub token from environment
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN is not set in this environment!")

# --- Optional: verify token works with GitHub API ---
resp = requests.get("https://api.github.com/user", headers={"Authorization": f"token {token}"})
if resp.status_code != 200:
    raise ValueError(f"GitHub token failed authentication: {resp.status_code} {resp.text}")
print("✅ GitHub token verified:", resp.json()["login"])

# --- Open repo ---
repo = Repo(repo_dir)

# Ensure we are on main branch
repo.git.checkout(branch)

# Copy file into repo
shutil.copy(file_to_push, os.path.join(repo_dir, file_to_push))

# Stage changes
repo.git.add(A=True)

# Commit if there are changes
if repo.is_dirty(untracked_files=True):
    repo.index.commit("Auto-update: AI model")
else:
    print("No changes to commit — will push anyway")

# Set remote URL with token and push main branch
origin = repo.remote(name="origin")
origin.set_url(f"https://x-access-token:{token}@github.com/aimodeler-demo/{username}.git")

# Push to GitHub and set upstream
push_info = origin.push(refspec=f"{branch}:{branch}", force=True, set_upstream=True)
print(push_info)


import os
import shutil
from git import Repo, GitCommandError

# --- Settings ---
username = "user01"
file_name = "AI_Modeler_Demo_01.py"
token = os.getenv("GITHUB_TOKEN")
repo_dir = "repos"

# Construct URL with basic auth format (more reliable for 403 errors)
url = f"https://{token}@github.com/aimodeler-demo/{username}.git"

# 1. Initialize / Open Repo
if not os.path.exists(repo_dir):
    repo = Repo.clone_from(url, repo_dir)
else:
    repo = Repo(repo_dir)

# 2. Copy the file into the repo folder
dest_path = os.path.join(repo_dir, file_name)
shutil.copy2(file_name, dest_path)

# 3. Force Git to see the change
repo.git.add(file_name)

try:
    # 4. Commit (only if there is something to commit)
    repo.index.commit("Update model")
    print("Commit created.")
except:
    print("No changes to commit (local matches remote).")

# 5. The Authentication Fix
try:
    # Reset the origin URL to ensure the token is embedded correctly
    if 'origin' in repo.remotes:
        repo.delete_remote('origin')
    origin = repo.create_remote('origin', url)
    
    print("Pushing to GitHub...")
    # Force push to 'main'
    origin.push(refspec='HEAD:main', force=True)
    print("✅ Success! Check GitHub.")
    
except GitCommandError as e:
    print(f"❌ Still getting 403. Check your Token Permissions on GitHub.\nError: {e}")

import faiss
import numpy as np

def knowledge_base(query):

    index = faiss.read_index("vector_store.index")

    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=query
    )
    query_embedding = np.array([response.data[0].embedding], dtype="float32")

    D, I = index.search(query_embedding, k=3)

    retrieved_chunks = []
    retrieved_sources = []

    for i in I[0]:
        if i < len(chunks):
            retrieved_chunks.append(chunks[i])
            retrieved_sources.append(chunk_filenames[i])

    if not retrieved_chunks:
        text = None
        return None

    text = "\n\n".join(
        f"[Source: {src}]\n{text}" for src, text in zip(retrieved_sources, retrieved_chunks)
    )

    return text

# Sync Timestamp: Mon Jan 26 23:58:33 2026
# Main Sync: Tue Jan 27 00:01:51 2026
# Main Sync: Tue Jan 27 00:03:58 2026
# Main Sync: Tue Jan 27 00:05:38 2026
# Main Sync: Tue Jan 27 11:07:00 2026