import structuralmetric as sm
import termfrequency as tf
import interpreter
import os


def main():
    folder = 'templates'
    repo1 = input('Enter repository: ')

    filename = os.path.join(folder, repo1 + '.json')
    user_repo = sm.load_structure(filename)

    scores = []

    for f in sorted(os.listdir(folder)):
        if f.endswith('.json'):
            filename = os.path.join(folder, f)
            structure = sm.load_structure(filename)
            score = sm.set_similarity(structure, user_repo)

            scores.append((f, score))
    
    smscores = sorted(scores, key=lambda x: x[1], reverse=True)
    tfrepos = tf.tfidf(repo1)

    count = 0

    similar_repos = []

    for score in smscores[1:]:
        if count > 2:
            break
        if score[1] >= 0.2:
            similar_repos.append(score[0][:-5])
            print(score[0][:-5])
            count += 1
    
    
    for repo in tfrepos:
        if count > 2:
            break
        if repo[0] not in similar_repos:
            print(repo[0])
            count += 1
    
    
    if count == 0:
        print('No similar templates')
    else:
        repo2 = input('Enter second repository from list: ')
        interpreter.compare(repo1, repo2)



if __name__ == "__main__":
    main()