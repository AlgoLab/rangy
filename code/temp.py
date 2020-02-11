import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
from itertools import combinations
import Node, Tree

def labels_set(t):
    #using set of words to get separated labels from the tree.
    #'set' construct makes them unique even tho they alredy should be
    L = set(t.replace('\n', ' ').split())
    return L

#
#Funzione per associare in un dizionario labels testuali a sequenza di int?
#

def permutation(t, c1, c2):
    #helper func for exchanging 2 elements of the string, whitespace separated  
    t = t.replace(c1, 'z')
    t = t.replace(c2, c1)
    t = t.replace('z', c2)
    return t

def permutation_full_tree(t):
    #prepare empty set and 'L' set of labels, list all the unique combinations
    #of labels pairs, iterate this list and apply 'permutation(t, p[0], p[1])'
    #add the returned value to the set, and return the set of
    #unique 1d trees permutations
    set_d1_t = set()
    L = labels_set(t)
    perms = list(combinations(L, 2))
    for p in perms:
        set_d1_t.add(permutation(t, p[0], p[1]))
    return set_d1_t

def permutation_brute(trees):
    #for every t (tree in the set 'trees') call permutation_full_tree(t)
    #join returned set to the common set and return in bulk at the end
    big_set_t = set()
    for t in trees:
        #print('current tree:')
        #print(t)
        big_set_t = big_set_t.union(permutation_full_tree(t))
        #print(list(big_set_t))
    return big_set_t

def lc_subsets(t):
    L = labels_set(t)
    lc_subsets = {}
    t_string = t.replace(' ', '').replace('\n', '')
    for l in L:
        lc_subsets[l]=t_string
        for n in t.splitlines():
            if l == n[0]:
                for c in n[1:].replace(' ',''):
                    lc_subsets[l] = lc_subsets[l].replace(c, '')
            if l in n[1:]:
                lc_subsets[l] = lc_subsets[l].replace(n[0], '')
    
    return lc_subsets

def link_and_cut(t, v, w):
    ls = t.splitlines(True)
    new_t = ''
    for l in ls:
        if v in l[1:]:
            new_t += l.replace(' '+v, '')
        if w in l[0]:
            new_t += l.replace('\n', ' '+ v +'\n')
        else:
            new_t += l
    
    return new_t

def link_and_cut_outer(t):
    #Dal punto di vista di Adj_list bisogna prendere un nodo (eligible for 
    # link and cut), figlio e appenderlo in fondo ad un'altra riga (non dei 
    # suoi discendenti)

    #applicare splitlines all'albero di origine, e ciclare su 'l' in 'L' meno le
    # righe della discendenza di 'l' ('l' stesso escluso)
    #tree_lines = t.splitlines(True)
    #for l in L:
    #   Subset =  L - disc(l)   #compreso 'l'
    #   for s in Subset:
    #       link_and_cut(T, l, s)
    #def link_and_cut(v, w):

    subsets = lc_subsets(t)
    lc_tree_set = set()
    for v, nodes in subsets.items():
        for w in nodes:
            lc_tree_set.add(link_and_cut(t, v, w))
    return lc_tree_set


def main(): 
    with open('input4.txt', 'r') as f:
        tree1 = f.read()
    d1 = permutation_full_tree(tree1)           #NB a d1 non c'è l'albero iniziale, ma ritorna a d2, aggiungermo a mano?
    d2 = permutation_brute(d1)
    d3 = permutation_brute(d2)
    d4 = permutation_brute(d3)
    #print(list(d1))
    #print(list(d2))
    #print(list(d3))
    #print(list(d4))
    print(len(d1))
    print(len(d2))
    print(len(d3))
    print(len(d4))
    print(sorted(d4))
    prufer = set()
    for t in d4:
        g=nx.parse_adjlist(t.splitlines(), nodetype=int)
        prufer.add(repr(nx.to_prufer_sequence(g)))

    print('prufer list:')
    print(sorted(prufer))


if __name__ == "__main__":
    main()