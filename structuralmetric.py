import json

# Function to save dictionaries as json
def save_structure(structure, filename, fun=None):

    with open(filename, 'w') as f:
        json.dump(structure, f, indent=4, default=fun)

# Function to load json
def load_structure(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Count number of files and directories
def count_items(d):
    ignore = {'dirs', 'files', 'sha'}
    count = 0
    for key, value in d.items():
            if key in ignore:
                 if isinstance(value, dict):
                      count += count_items(value)
            else:
                count += 1

                if isinstance(value, dict):
                     count += count_items(value)

    return count


# Make sets from the files and directories and hashes
def get_sets(d, path='root'):
    files = set()
    directories = set()

    for key, value in d.items():
            if key == 'files':
                for k, v in value.items():
                    files.add((path, k, v['sha']))
            
            if key == 'dirs':
            
                for k, v in value.items():

                    new_path = path + '/' + k


                    if k != 'dirs' and k != 'files':
                        directories.add((path, k))
                     
                    sub_files, sub_directories = get_sets(v, new_path)

                    files.update(sub_files)
                    directories.update(sub_directories)

    return files, directories



# Reconstruct the largest common struture between the two trees
def largest_common_component(d1, d2):
    s1_files, s1_dirs = get_sets(d1)
    s2_files, s2_dirs = get_sets(d2)

    matching_files = s1_files & s2_files
    matching_dirs = s1_dirs & s2_dirs

    structure = build('root', matching_dirs, matching_files)
    return structure

# Build nested directory structure
def build(parent, dirs, files):

    result = {"dirs": {}, "files": {}}

    for file in files: 
        if file[0] == parent:          
            result["files"][file[1]] = file[2]

    for dir in dirs:
        if dir[0] == parent:
            result["dirs"][dir[1]] = build(parent + '/' + dir[1], dirs, files)


    return result

# Build set of different subtrees
def difference(d1, d2):
    s1_files, s1_dirs = get_sets(d1)
    s2_files, s2_dirs = get_sets(d2)

    different_files = (s1_files - s2_files)
    different_dirs = s1_dirs - s2_dirs

    forest = {}

    root_dirs, root_files = get_roots(different_dirs, different_files)
    
    for path in root_dirs:
        for dir in different_dirs:
            if dir[0] == path:
                structure = build(path, different_dirs, different_files)
                forest[path] = structure
    
    for path in root_files:
        for file in different_files:
            if file[0] == path:
                forest[path] = {file[1] : file[2]}
                
    return forest
    
    

# Get roots of the locations of altered subtrees
def get_roots(dirs, files):

    roots_dirs = set()
    roots_files = set()

    for dir in dirs:
        path = dir[0]

        flag = True
        for d in dirs:
            if path == d[0] + '/' + d[1]:
                flag = False
        
        if flag:
            roots_dirs.add(path)

    for file in files:
        path = file[0]

        if path in roots_files:
            continue

        path_parts = path.split('/')

        flag = True
        for i in range(1, len(path_parts)+ 1):
            sub_path = '/'.join(path_parts[:i])
            if sub_path in roots_dirs:
                flag = False

        if flag:
            roots_files.add(path)

    return roots_dirs, roots_files
        

# Compute similarity score by counting the numer of items in the reconstructed structure divided by the number in the original
def set_similarity(d1, d2):

    s1_files, s1_dirs = get_sets(d1)
    s2_files, s2_dirs = get_sets(d2)

    matching_files = s1_files & s2_files
    matching_dirs = s1_dirs & s2_dirs

    matching_elements = matching_files.union(matching_dirs)   

    total = (len(s1_files.union(s1_dirs)) + len(s2_files.union(s2_dirs)))/2
    return(len(matching_elements)/total)
