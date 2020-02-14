import networkx as nx
from itertools import combinations
from queue import SimpleQueue

def labels_set(t):
    #Using set of words to get separated labels from the tree.
    #'set' construct makes them unique even tho they alredy should be.
    L = set(t.replace('\n', ' ').split())
    return L

#
#Funzione per associare in un dizionario labels testuali a sequenza di int?
#

def permutation_inner(t, c1, c2):
    #Helper func for exchanging 2 elements of the string, whitespace separated.  
    t = t.replace(c1, 'z')
    t = t.replace(c2, c1)
    t = t.replace('z', c2)
    return t

def permutation_single_tree(t):
    #Prepare empty set and 'L' set of labels, list all the unique combinations
    # of labels pairs, iterate this list and apply 
    # 'permutation_inner(t, p[0], p[1])'. Add the returned value to the set, 
    # and return the set of unique 1d trees permutations.
    set_d1_t = set()
    L = labels_set(t)
    perms = list(combinations(L, 2))
    for p in perms:
        set_d1_t.add(permutation_inner(t, p[0], p[1]))
    return set_d1_t

def permutation(trees):
    #For every t (tree in the set 'trees') call permutation_single_tree(t).
    # Join returned set to the common set and return in bulk at the end.
    big_set_t = set()
    for t in trees:
        big_set_t = big_set_t.union(permutation_single_tree(t))
    return big_set_t

def bfs(t, v):
    #Given a tree 't' and a node 'v' of that tree, return the set of nodes 
    # which descend from 'v'.
    ls=t.splitlines()
    q = SimpleQueue()
    q.put(v)
    lb_set = set()
    while not q.empty():
        qq = q.get()
        lb_set.add(qq)
        for l in ls:
            if l.split()[0] == qq:
                for c in l.split()[1:]:
                    q.put(c)
                break
    return lb_set

def get_father(t, v):
    #Given a tree 't' and a node 'v', return the father of 'v'.
    ls = t.splitlines()
    a = ''
    for l in ls:
        if v in l.split()[1:]:
            a = l.split()[0]
            break
    return a

def lc_subsets(t):
    #Given a tree 't' return a dictionary with the labels of the tree as keys 
    # and as values the list of nodes eligible for link-and-cut operation for 
    # each of the nodes.
    L = labels_set(t)
    lc_subsets = {}
    for l in L:
        lc_subsets[l]=L.copy()
        rm_labels=bfs(t, l)
        rm_labels.add(get_father(t, l))
        lc_subsets[l].difference_update(rm_labels)

    return lc_subsets

def link_and_cut_inner(t, v, w):
    #Basic link-and-cut operation between 'v' and 'w'. Where 'w' becomes the 
    # new father.
    ls = t.splitlines(True)
    new_t = ''
    for l in ls:
        if v in l.split()[1:]:
            new_t += l.replace(' '+v, '')
        elif w in l.split()[0]:
            new_t += l.replace('\n', ' '+ v +'\n')
        else:
            new_t += l
    
    return new_t

def lc_clean_set(s):
    #given a set of trees, check for trees which comes with bad ordering after 
    # link-and-cut operations, reorder their adj_list representation and return
    # the new 'clean' set.
    new_s = set()
    while len(s) != 0:
        t = s.pop()
        L = labels_set(t)
        L.remove('0')
        for l in L:
            if t.index('\n'+l) < t.index(' '+l):
                t=t.replace('\n'+l, '')
                t+='\n'+l
        new_s.add(t)
    return new_s

def link_and_cut_single_tree(t):
    #Given a tree 't', returns all the resulting trees after one link-and-cut 
    # operation, for every possible link-and-cut operation possible for the 
    # given tree. In the end it's needed to call 'lc_clean_set()' because after 
    # applying a link-and-cut operation trees representerd in adj_list can 
    # result correct in structure but disordered in presentation, so a 
    # reordering or the rows is needed.
    subsets = lc_subsets(t)
    lc_tree_set = set()
    for v, nodes in subsets.items():
        for w in nodes:
            lc_tree_set.add(link_and_cut_inner(t, v, w))
    return lc_clean_set(lc_tree_set)

def link_and_cut(trees):
    #Outer link_and_cut func. Given a set of trees, return a set containing all 
    # the d1 link-and-cut trees from every tree in the starting set.
    ret_set = set()
    for t in trees:
        ret_set = ret_set.union(link_and_cut_single_tree(t))
    return ret_set

def main(): 
    with open('input/input4.txt', 'r') as f:
        tree1 = f.read()
    #d1 = permutation_single_tree(tree1)            #NB: a d1 non c'è l'albero 
    #d2 = permutation(d1)                           #iniziale, ma ritorna a d2, 
    #d3 = permutation(d2)                           #aggiungermo a mano?
    #d4 = permutation(d3)

    #prufer = set()
    #for t in d4:
    #    g=nx.parse_adjlist(t.splitlines(), nodetype=int)
    #    prufer.add(repr(nx.to_prufer_sequence(g)))#
    #print('prufer list:')
    #print(sorted(prufer))

    lc = link_and_cut_single_tree(tree1)
    print(lc_subsets(tree1))
    print(lc)

if __name__ == "__main__":
    main()