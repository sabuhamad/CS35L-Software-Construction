#!/usr/bin/python3

# run strace to verify this does not use
# other commands

import os
import sys
import zlib


# creates the CommitNode class to store hash, listofparents, and children
class CommitNode:
    def __init__(self, hash):
        """
        :type hash: str
        """
        self.hash = hash
        self.listofparents = set()
        self.children = set()


# returns commit message
def getmessage(text):
    lines = text.splitlines()
    enumerate(lines)
    message = lines[-1]
    return message


# returns a list of parents of the commit
def getparent(text):
    lines = text.split()
    listofparents = []
    enumerate(lines)
    for i in range(len(lines)):
        if lines[i-1] == 'parent':
            listofparents.append(lines[i])
    return listofparents


# main function for processing topological order of commits
def topo_order_commits():
    currentpath = os.getcwd()
    repository = False
    while currentpath != "/":
        if os.path.isdir(currentpath + "/.git"):
            repository = True
            break
        else:
            currentpath = os.path.dirname(currentpath)
    if not repository:
        sys.stderr.write("Error: Currently not in Valid Git Repository")
        sys.exit(1)
    pathtohead = currentpath + "/.git/refs/heads"
    object_path = currentpath + "/.git/objects"
    heads = []
    for root, dirs, files in os.walk(pathtohead, topdown=False):
        for name in files:
            heads.append(os.path.join(root, name))
    discovered_node = dict()
    head_map = dict()
    head_hash = []
    for head in heads:
        f = open(head, 'r')
        text = f.read().strip()
        f.close()
        if text not in head_map:
            i = head.replace((pathtohead + '/'), '')
            head_map[text] = [i]
        else:
            i = head.replace((pathtohead + '/'), '')
            head_map[text].append(i)
            new_data = sorted(head_map[text])
            head_map[text] = new_data
        head_hash.append(text)
    for sha in head_hash:
        stack = []
        f = open((object_path + "/" + sha[:2] + "/" + sha[2:]), 'rb')
        text = (zlib.decompress(f.read().strip())).decode('utf-8')
        f.close()
        listofparents = getparent(text)
        if sha not in discovered_node:
            discovered_node[sha] = CommitNode(getmessage(text))
        discovered_node[sha].listofparents.update(listofparents)
        stack.extend(listofparents)
        for node in discovered_node[sha].listofparents:
            if node not in discovered_node:
                discovered_node[node] = CommitNode("")
            discovered_node[node].children.add(sha)

        # check parents of commit
        while len(stack) != 0:
            end = stack[-1]
            stack.pop()
            fs = open((object_path + "/" + end[:2] + "/" + end[2:]), 'rb')
            old_texts = zlib.decompress(fs.read())
            textd = old_texts.decode('utf-8')
            texts = textd.strip()
            fs.close()
            listofparents = getparent(texts)
            discovered_node[end].listofparents.update(listofparents)
            discovered_node[end].hash = getmessage(texts)
            for node in discovered_node[end].listofparents:
                if node not in discovered_node:
                    stack.append(node)
                    discovered_node[node] = CommitNode("")
                discovered_node[node].children.add(end)
    dictionary = {}
    for key, x in discovered_node.items():
        copied_node = CommitNode(x.hash)
        copied_node.listofparents = x.listofparents.copy()
        copied_node.children = x.children.copy()
        dictionary[key] = copied_node
    queue = []
    topo_sort = []
    while len(dictionary) != 0:
        for node in dictionary:
            if len(dictionary[node].children) == 0:
                if node not in queue:
                    queue.insert(0, node)
        top = queue[-1]
        queue.remove(top)
        topo_sort.append(top)
        for node in dictionary[top].listofparents:
            dictionary[node].children.remove(top)
        dictionary.pop(top)
    topo_sort.extend(queue)
    prev_str = ""
    while (topo_sort):
        curr_node = topo_sort[0]
        topo_sort.remove(curr_node)
        if prev_str != "":
            if prev_str[-2:] == "=\n":
                temp = ""
                for child_node in discovered_node[curr_node].children:
                    temp += (child_node + " ")
                print("=" + temp[:-1])

        # add branch if they are heads
        print_str = curr_node
        if curr_node in head_map:
            for branch_name in head_map[curr_node]:
                print_str += (" " + branch_name)
        prev_str = print_str
        print(print_str)
        print_str = ""
        temp = ""
        if len(topo_sort) == 0:
            break
        next_node = topo_sort[0]
        if curr_node not in discovered_node[next_node].children:
            if (discovered_node[curr_node].listofparents):
                for parent in discovered_node[curr_node].listofparents:
                    temp += (parent + " ")
                print_str = temp[:-1]
            print_str += "=\n"
            prev_str = print_str
            print(print_str)


if __name__ == '__main__':
    topo_order_commits()
