import argparse
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
    #Given a set of trees, check for trees which comes with bad ordering after 
    # link-and-cut operations, reorder their adj_list representation and return
    # the new 'clean' set.
    new_s = set()
    while len(s) != 0:
        t = s.pop()
        L = labels_set(t)
        L.remove('0')
        for l in L:
            if t.index('\n'+l) < t.index(' '+l):
                for x in t.splitlines():
                    if x[0] == l:
                        r = x
                t=t.replace('\n'+r, '')
                t+=r+'\n'
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

def prufer_check(s1, s2):
    #Given 2 sets, one is trees from permutations, the other is tree from 
    # link-and-cut, convert every tree into Prufer sequence using Networkx, 
    # filter duplicates and then looks for matches between the 2 sets. 
    # Return a report(?).
    prufer1 = set()
    prufer2 = set()
    report = ''
    for t1 in s1:
        g1=nx.parse_adjlist(t1.splitlines(), nodetype=int)
        prufer1.add(repr(nx.to_prufer_sequence(g1)))
    for t2 in s2:
        g2=nx.parse_adjlist(t2.splitlines(), nodetype=int)
        prufer2.add(repr(nx.to_prufer_sequence(g2)))
    
    print(prufer1)
    print('---------------------------------------------------------------')
    print(prufer2)

    for p in prufer1:
        if p in prufer2:
            report += '> The tree '+ p +' was found in both sets.\n'
    if report == '':
        report +='> No matches.'
    
    return report

def exh_search(t1, t2, n):
    #Given 2 trees 't1' and 't2', and an integer 'n', for 'n' times, iterate 
    # 'permutations()' on 't1' and 'link_and_cut()' on 't2'. 
    # Then call 'prufer_check()' on the resulting sets and return the report.
    report = 'Here the result for exhausting search at distance '+str(n)+'\n'
    s1 = permutation_single_tree(t1)
    s2 = link_and_cut_single_tree(t2)
    s1.add(t1)
    s2.add(t2)
    
    for _ in range(n-1):
        s1.update(permutation(s1))
        s2.update(link_and_cut(s2))
    report += prufer_check(s1, s2)
    return report

def main():
    parser = argparse.ArgumentParser(description='''Given 2 trees (in AdjList 
        format) perform exhaustive search for permutations and link-and-cut 
        trees at a certain distance(default=1) and check if the two operations 
        generate the same tree from a different starting tree.''')
    parser.add_argument('t1', help='''path to the txt file containing the 
        first origin tree''')
    parser.add_argument('t2', help='''path to the txt file containing the 
        second origin tree''')
    parser.add_argument('n', type=int, nargs='?', const=1, default=1, 
        help='''The number of iterations for each algorithm. Default is 1, so 
        calculate every tree possible with only 1 permutation/link-and-cut, 
        for n=2 every tree possible with 2 permutations/link-and-cuts and so 
        forth''')
    args = parser.parse_args()

    with open(args.t1, 'r') as f1:
        tree1 = f1.read()

    with open(args.t2, 'r') as f2:
        tree2 = f2.read()
    report = exh_search(tree1, tree2, args.n)

    #with open('input/input4.txt', 'r') as f1:
    #    tree1 = f1.read()
#
    #with open('input/input4_d1.txt', 'r') as f2:
    #    tree2 = f2.read()
    #report = exh_search(tree1, tree2, 2)
    print(report)
    
if __name__ == "__main__":
    main()