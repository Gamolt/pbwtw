import sys

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
    #vado a cambiare il valore '*' con il valore t, mi serve un valore int
    for i in range(len(sequence)):
        sequence[i] = [int(j) if j is not '*' else t for j in sequence[i]]
    
    sequence = list(map(list, zip(*sequence)))
   
    a.append([i for i in range(len(sequence[0]))])
    d.append([0 for i in range(len(sequence[0]))])

    for i in range(len(sequence)):
        for i, l in zip(compute_next_array(sequence[i], [k for k in a[i]], [j for j in d[i]], t, i), [a, d]):
            l.append(i)
    
    return a, d

a, d = main(int(sys.argv[1]), sys.argv[2])
print('a vector: ', a[1:])
print('d vector: ', d[1:])