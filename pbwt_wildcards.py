import sys



def search_first_block(a, d, j):
    block = []
    
    i = 0
    x,y = ([] for i in range(2))
    for r in range(1,len(d)):

        if d[r] == j and r != 1 and r != len(d)-1:
            block.append((a[i:r], d[r-1], j))
            i=r
        
        if r == len(d)-1:
            block.append((a[i:r+1], d[r-1], j))
                
    return block

def search_block(a, d, j, b, wildcard):
    block = []
    
    i = 0
    x,y = ([] for i in range(2))
    for r in range(1,len(d)):

        if r == 1 and d[r]==j:
            i=r
        elif d[r] == j and r != 1 and r != len(d)-1:
            block.append((a[i:r], max(d[i+1:r]), j))
            i=r

        elif r == len(d)-1:
            block.append((a[i:r+1], max(d[i+1:r+1]), j))
 
                
    return check_block(b, consensus_check(block, wildcard), j, wildcard)

#b è la lista di blocchi precedenti, block è quella nuova
def check_block(b, block, n, wildcard):
    k = list(b)
    l = list(block)


    for j in b:
        count = len([x for x in j[0] if x in block[0][0]])
 
        if count == len(j[0]):
            if len(block[0][0]) == count:
                k.remove(j)
            else:
                k.remove(j)
                if j ==([0, 2, 3], 1, 2): print('second')
                l.append((j[0], j[1], l[0][2]))

            if j ==([0, 2, 3], 1, 2): print('first')

        elif (len(j[0]) < count or len(j[0]) > count) and count != 0:
            if j ==([0, 2, 3], 1, 2): print('third')
            zero = []
            one = []

            for x in j[0]:
                if x in block[0][0]:
                    zero.append(x)
                else:
                    one.append(x)
            if len(zero) > 1:
                l.append((zero, j[1], l[0][2]))
            if len(one) > 1:

                l.append((one, j[1], l[0][2]))

            copy = list(l)

            for f in l:
                if copy.count(f) > 1:
                    copy.remove(f)
            l = list(copy)

        #Vuol dire che ha un simbolo diverso
        elif count == 0:
            count = len([x for x in j[0] if x in block[1][0]]) 
            if count == len(j):
                k.remove(j)

            if count < len(j):
                k.remove(j)
                l.append((j[0], j[1], l[0][2]))


    return consensus_check(k, wildcard), l

def consensus_check(block, wildcard):
    b = list(block)

    for i in block:
        for j in range(i[1], i[2]):
                res = all(elem in wildcard[j] for elem in i[0])
                if res:
                    b.remove(i)

    return b

def collapse(a, d):
    aa, dd = ([] for i in range(2))
    j = 0

    while j < len(a):
        while j+1 != len(a) and a[j] == a[j+1]:
            j += 1
            
        aa.append(a[j])
        dd.append(d[j])

        j += 1

    return aa, dd 

#xk = valori colonne reali, ak array prefissi, dk array divergenza,
#t numero simbolo all'interno dell'alfabeto, k posizione in cui viene
#effettuato il controllo.
#L'array u definito nel pseudocodice non verrò usato
#dato che giocherò sulle liste.    
def compute_next_array(xk, ak, dk, t, k):
    a, d = ([[] for i in range(t)] for j in range(2))
    a_star, d_star, p, u = ([] for i in range(4))
    dim = len(ak)

    for l in range(t):  
        u.append(0)
        p.append(k+1)

    for i in range(dim):
        allele = xk[ak[i]]
    
        for l in range(t):
            if dk[i] > p[l]:
                p[l] = dk[i]

        if allele == t:     
            for m in range(t):
                a[m].append(ak[i])
                d[m].append(p[m])
                p[m] = 0

        else:
            a[allele].append(ak[i])
            d[allele].append(p[allele])
            p[allele] = 0
            u[allele] += 1
  
    for i in range(t):
      
        for i, l in zip(collapse(a[i], d[i]), [a_star, d_star]):
            l.append(i)
      
    flatter = lambda l: [i for li in l for i in li]

    return flatter(a_star), flatter(d_star)


def main(t, file):
    a, d = ([] for i in range(2))
    f = open(file, 'r')
    sequence = []

    for i in f:
        sequence.append(i.rstrip('\n'))
    f.close()
    wildcard_list = ([[] for i in range(len(sequence[0]))])
    block = []

    #vado a cambiare il valore '*' con il valore t, mi serve un valore int
    for i in range(len(sequence)):
        sequence[i] = [int(j) if j is not '*' else t for j in sequence[i]]
    
    #wildcard_list avrà all'interno le posizioni in cui si troveranno le wildcard.
    for i in range(len(sequence)):
        for j in range(len(sequence[i])):
            if sequence[i][j] == t:
                wildcard_list[j].append(i)
    sequence = list(map(list, zip(*sequence)))

   
    a.append([i for i in range(len(sequence[0]))])
    d.append([0 for i in range(len(sequence[0]))])

    for i in range(len(sequence)):
        for q, l in zip(compute_next_array(sequence[i], [k for k in a[i]], [j for j in d[i]], t, i), [a, d]):
            l.append(q)
    
    for i in range(1,len(a)):
        if i == 1:
            block.append(search_first_block(a[i],d[i],i))
        else:

            block[-1], t = search_block(a[i],d[i],i, block[-1], wildcard_list)
            block.append(t)
    
    flatter = lambda l: [i for li in l for i in li]

    #block = consensus_check(flatter(block), wildcard_list)                

    return a, d, flatter(block)

a, d, b = main(int(sys.argv[1]), sys.argv[2])
print('a vector: ', a[1:])
print('d vector: ', d[1:])
print('number b: ', b)
