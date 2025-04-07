import re
import markdown
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


readmes = []
readme_vectors = []
repo_list = []

# Load json
def load(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Clean the read me files
def clean_markdown(content):
    html = markdown.markdown(content)
    soup = BeautifulSoup(html, "html.parser")

    for code_block in soup.find_all("code"):
        code_block.decompose()

    text = soup.get_text(separator=" ")
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text


# Clean read me files and save them as a vector
def clean(folder):
    count = 0
    for filename in sorted(os.listdir(folder)):
        if filename.endswith('.json'):
            filename = os.path.join(folder, filename)
            content = load(filename)
            readmes.append(content)
            name = os.path.basename(filename)
            name = os.path.splitext(name)[0]
            repo_list.append(name)

        if count > 300:
            break

        count += 1

# Vectorize readmes, compute cosine similarity matrix and extract the most similar list of entries with r
def vectorize(readmes, r):
    index_to_repo = {}
    repo_to_index = {}

    r = r + '_readme'

    for index, repo in enumerate(repo_list):
        index_to_repo[index] = repo
        repo_to_index[repo] = index
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(readmes)
    cosine_sim_matrix = cosine_similarity(tfidf)

    i = repo_to_index[r]

    result_list = cosine_sim_matrix[:, i].tolist()

    indices = np.argsort(result_list)[-4:][::-1]

    repos = []
    for j in indices[1:4]:
        repos.append((index_to_repo[j][:-7], result_list[j]))

    return repos



    
    


# Run the metric on a folder of read mes
def tfidf(repo):
    folder = 'readmes'
    clean(folder)
    return(vectorize(readmes, repo))