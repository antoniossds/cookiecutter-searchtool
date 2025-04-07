import structuralmetric as sm
import os
from openai import OpenAI
import json

client = OpenAI(
  api_key="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"
  )

input_folder = 'templates'
output_folder = 'output'

def interpret(lcc, diff1, diff2, readme1, readme2):
    prompt = (
        "Given the following largest common subtree:\n"
        f"{json.dumps(lcc, indent=4)}\n\n"
        "And the following differences in repo one:\n"
        f"{json.dumps(diff1, indent=4)}\n\n"
        "And the following read me for repo one:\n"
        f"{readme1}\n\n"
        "And the following differences in repo two:\n"
        f"{json.dumps(diff2, indent=4)}\n\n"
        "And the following read me for repo two:\n"
        f"{readme2}\n\n"
        "Please interpret what differences in functionality exist between these repositories which are both cookiecutters aimed at project templating."
    )

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": prompt}
    ] 
    )

    output = str(completion.choices[0].message)
    output = output.replace('\\n', '\n')
    print(output);

    filename = os.path.join(output_folder, 'interpreter_output.txt')
    with open(filename, 'w') as f:
            f.write(output)
    

    


def compare(r1, r2):
    
    filename = os.path.join(input_folder, r1 + '.json')
    repo1 = sm.load_structure(filename)

    filename = os.path.join(input_folder, r2 + '.json')
    repo2 = sm.load_structure(filename)

    lcc = sm.largest_common_component(repo1, repo2)
    diff1 = sm.difference(repo1, repo2)
    diff2 = sm.difference(repo2, repo1)

    
    filename = os.path.join('readmes', r1 + '_readme.json')
    with open(filename, 'r', encoding='utf-8') as f:
        readme1 = json.load(f)

    filename = os.path.join('readmes', r2 + '_readme.json')
    with open(filename, 'r', encoding='utf-8') as f:
        readme2 = json.load(f)
    

    interpret(lcc, diff1, diff2, readme1, readme2)
    