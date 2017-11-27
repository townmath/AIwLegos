
#from Lesson 1 Q26 from AI4R
BATCH=3
COLORS=3
COLOR_NAMES=['red','green','blue']

p=[1./(BATCH*COLORS) for prob in range(BATCH*COLORS)]
world=[COLOR_NAMES[num/3] for num in range(BATCH*COLORS)]
#print p
#print world
#['green', 'red', 'red', 'green', 'green']

measurements = ['red', 'red','white','green','green','green','white','blue','blue']
motions = [1,1,1]

#sense probabilities
pHit = 0.6
pMiss = 0.2

#move probabilities
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

def sense(p, Z):
    q=[]
    for i in range(len(p)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    s = sum(q)
    for i in range(len(q)):
        q[i] = q[i] / s
    return q

def move(p, U):
    q = []
    for i in range(len(p)):
        s = pExact * p[(i-U) % len(p)]
        s = s + pOvershoot * p[(i-U-1) % len(p)]
        s = s + pUndershoot * p[(i-U+1) % len(p)]
        q.append(s)
    return q

done=False
k=0
while not k==len(world)-1:
    print k
    measurement=measurements[k]
    p = sense(p, measurement)
    if measurement==world[k]:
        motion=1
    else:#bad block found
        motion=-1
        print "swing the golf club",
        print measurement, " is not ", world[k]
        measurements[k]=world[k]
    p = move(p, motion)
    k=p.index(max(p))

print p
