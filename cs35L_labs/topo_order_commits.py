import os
import sys
import zlib
import copy
from collections import deque

#checks if directory exists, returns if so
def is_directory():
    c_path = os.getcwd()
    path_exist = os.path.exists(c_path + '/.git')
    while(not path_exist):
        if(c_path == '/'):
            print("Not in a git repository")
            sys.exit()
        c_path = os.path.dirname(c_path)
        path_exist = os.path.exists(c_path + '/.git')
    return c_path + '/.git'

#gets the branches from the respective git directory
def get_branches(git_dir):
    branches = {}
    for (dirpath,dirnames,filenames) in os.walk(git_dir + '/refs/heads'):
        continue
    for f in filenames:
        names = open(dirpath + '/' + f,'r')
        br = dirpath[len(git_dir + '/refs/heads') + 1:]
        if(br != ''):
            br += '/' + f
        else:
            br = f
        branches[br] = names.read()[:-1]
    return branches

class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

#creates commit graph using dfs
#keep going through hashes until one doesnt have parent
def build_commit_graph(git_dir, branches):
    hashes = []
    for b in branches:
        hashes.append(branches[b])
    seen = {}
    hash_to_node = {}
    stack = hashes
    while (len(stack)>0):
        curr_hash = stack.pop()
        if curr_hash not in seen:
            seen[curr_hash] = 1
            if curr_hash not in hash_to_node:
                hash_to_node[curr_hash] = CommitNode(curr_hash)
            commit = hash_to_node[curr_hash]
            check_hash = open(git_dir + '/objects/' + curr_hash[:2] + '/' + curr_hash[2:],'rb')
            hash_decoded = zlib.decompress(check_hash.read()).decode()
           #find parent hash by splitting new line, finding string "parent"
            lines = hash_decoded.split('\n')
            for line in lines:
                if(line[:6] == 'parent'):
                    commit.parents.add(line[7:])
                    #print("Hello commit " + str(commit.commit_hash) + " " + str(commit.parents))
            for parent in commit.parents:
                if parent not in seen:
                    stack.append(parent)
                if parent not in hash_to_node:
                    hash_to_node[parent] = CommitNode(parent)
                hash_to_node[parent].children.add((curr_hash))
            #c_node = CommitNode(curr_hash)
    #print(seen)
    #print(hashes)
    #print(hash_to_node)
    #print(git_dir)
    return hash_to_node

#create a topological ordering through kahns algorithm
def gen_topo_ordering(commits):
    res = []
    commits_copy = copy.deepcopy(commits)
    leafs = deque()
    for c_hash in commits_copy:
        #print(commits_copy[c_hash].children)
        if(len(commits_copy[c_hash].children) == 0):
            leafs.append(c_hash)
    while(len(leafs)>0):
        c_hash = leafs.popleft()
        res.append(c_hash)
        for parent in list(commits_copy[c_hash].parents):
            commits_copy[c_hash].parents.remove(parent)
            commits_copy[parent].children.remove(c_hash)
            if(len(commits_copy[parent].children) == 0):
                leafs.append(parent)
    if(len(commits_copy) > len(res)):
        raise Exception("cycle")
    return res

def print_commit_hashes(top_sort_commits, commit_nodes, br_dict):
    check = False
    count = 0
    for i in top_sort_commits:
        curr_hash = i
        if check:
            check = False
            joined = ' '.join(commit_nodes[i].children)
            print('=' + joined)
        if(i in br_dict):
            branches = sorted(br_dict[i])
        else:
            branches = []
        if(len(branches)>0):
            print(curr_hash + ' ' + str(' '.join(sorted(br_dict[curr_hash]))))
        else:
            print(curr_hash + '')
        if((count+1 < len(top_sort_commits)) and (top_sort_commits[count+1] not in commit_nodes[curr_hash].parents)):
            check = True
            joined = ' '.join(commit_nodes[curr_hash].parents)
            print(joined + '=' + '\n')
        count += 1

def get_all_branches(branches):
    br_dict = {}
    for br in branches:
        br_dict[branches[br]] = br_dict.get(branches[br],[])
        br_dict[branches[br]].append(br)
    return br_dict

def topo_order_commits():
    directory = is_directory()
    branches = get_branches(directory)
    unsorted_commits = build_commit_graph(directory,branches)
    topo_ordering = gen_topo_ordering(unsorted_commits)
   # print_commit_hashes(topo_ordering)
    br_dict = get_all_branches(branches)
    print_commit_hashes(topo_ordering,unsorted_commits,br_dict)
if __name__ == '__main__':
    topo_order_commits(
            )
#I did not use any tricks to get the git objects/branches
#No git commands were used
