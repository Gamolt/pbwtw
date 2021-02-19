#lettura file da fixare
f = open("test.txt", "r")
l = []
for i in f:
    l.append(i.rstrip("\n"))

f.close()

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
    print('u: ', u)
    print('p: ', u)

    for i in range(dim):
        allele = xk[ak[i]]
    
        for l in range(t):
            if dk[i] > p[l]:
                p[l] = dk[i]
                print('Enter in dk check')

        if allele == '*':       
            print(allele)
            print(a, d, p, u)
            for m in range(t):
                a[m].append(ak[i])
                d[m].append(p[m])
                p[m] = 0
    
        else:
            a[allele].append(ak[i])
            d[allele].append(p[allele])
            p[allele] = 0
            u[allele] += 1

            print(i, ' step')
            print('a ', a)
            print('d ', d)
            print('p ', p)
            print('u ', u)

    for i in range(t):
        print(a[i])
        for i, l in zip(collapse(a[i], d[i]), [a_star, d_star]):
            l.append(i)
      
    flatter = lambda l: [i for li in l for i in li]

    return flatter(a_star), flatter(d_star)

print(compute_next_array([0,1,0], [0,1,2], [0,0,0], 2, 1))
#print(collapse([0,1,0], [0, 2, 1], [2, 0, 2]))