
file=open('/Users/deng/Desktop/network attack&defense/program/office/msoff/3.txt','a')
for a in range(10):
    for b in range(10):
        for c in range(10):
            for d in range(10):
                for e in range(10):
                    for f in range(10):
                        for g in range(10):
                            for h in range(10):
                                if (a!=h and b!=h and c!=h and d!=h and e!=h and f!=h and g!=h and g!=a and g!=e and g!=b and g!=c and g!=d and g!=f and f!=a and f!=b and f!=c and f!=d and f!=e and e!=a and e!=b and e!=c and e!=d and d!=a and d!=b and d!=c and c!=a and c!=b and a!=b):
                                    file.write(str(a)+str(b)+str(c)+str(d)+str(e)+str(f)+str(g)+str(h)+'\n')

