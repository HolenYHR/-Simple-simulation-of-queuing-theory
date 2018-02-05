import random as rm
import numpy
import matplotlib.pyplot as plt
tf=[0 for h in range(3)]
tb=[0 for l in range(3)]

lenofque=[[] for qq in range(3)]
A=[[] for m in range(3)]
D=[[] for n in range(3)]
Wait=[[] for pppp in range(3)]
lamd=[30,30,30]
mu=100
counter=[1 for q in range(3)]
counter2=[0 for e in range(3)]
nextFinish=0
polling=0
meannn=0
Total=1000000
SIZE=[[] for dd in range(3)]
num=0
ccc=0
totaltime=0
def Simulation():
    global polling,counter,ccc,A,counter2,D,nextFinish,meannn,num,time,totaltime,lamd
    for i in range(3):
        tf[i]=tb[i]=rm.expovariate(lamd[i])
        A[i].append(tf[i])
        lenofque[i].append(counter[i])
        totaltime=totaltime+tf[i]
    for j in range(3):
        if tf[j]<tf[polling]:
            polling=j
    ccc=3
    nextFinish=tf[polling]
    while ccc<=Total:

        if(tf[polling]<=nextFinish):
            tt=tb[polling]=tb[polling]+rm.expovariate(lamd[polling])
            while tt<nextFinish and ccc<Total:

                tb[polling]=tt
                A[polling].append(tb[polling])
                counter[polling]=counter[polling]+1
                ccc=ccc+1
                time=rm.expovariate(lamd[polling])
                totaltime=totaltime+time
                tt = tb[polling]+time
                lenofque[polling].append(counter[polling])
            scale=rm.expovariate(mu)
            meannn+=scale
            D[polling].append(nextFinish)
            SIZE[polling].append(scale)
            num+=1
            #print("number",num,"station",polling,"THISCOME",A[polling][counter2[polling]],"nextFinish",nextFinish," Scale",scale)
            nextFinish = nextFinish + scale
            Wait[polling].append(D[polling][counter2[polling]]-A[polling][counter2[polling]])
            counter[polling]=counter[polling]-1

            #print("couter",counter[polling])
            if counter[polling]==0 and ccc<Total:

                tb[polling]=tf[polling]=tf[polling]+rm.expovariate(lamd[polling])
                totaltime+=tf[polling]
                ccc=ccc+1
                A[polling].append(tf[polling])
                counter2[polling]=counter2[polling]+1
                counter[polling]+=1
                lenofque[polling].append(counter[polling])
            elif counter[polling]!=0:
                counter2[polling] = counter2[polling] + 1

                tf[polling]=A[polling][counter2[polling]]
            else:
                tf[polling]=10000000
            polling =(polling+1)%3

        else:
            for i in range(3):
                if tf[i]<=tf[polling]:
                    polling=i
            if tf[polling]==10000000:
                break
            if tf[polling]>=nextFinish:
                nextFinish=tf[polling]
def PlotGraph(array1,array2,array3):
    H1, X1 = numpy.histogram(array1, bins=70, normed=True)
    dx = X1[1] - X1[0]
    f1 = numpy.cumsum(H1) * dx
    # X2=numpy.sort(servicetime)
    # f2=numpy.array()
    plt.plot(X1[1:], 1 - f1,label="queue1")
    plt.semilogy()

    H2, X2 = numpy.histogram(array2, bins=70, normed=True)
    dx = X2[1] - X2[0]
    f2 = numpy.cumsum(H2) * dx
    # X2=numpy.sort(servicetime)
    # f2=numpy.array()
    plt.plot(X2[1:], 1 - f2,label="queue2")
    plt.semilogy()

    H3, X3 = numpy.histogram(array3, bins=70, normed=True)
    dx = X3[1] - X3[0]
    f3 = numpy.cumsum(H3) * dx
    # X2=numpy.sort(servicetime)
    # f2=numpy.array()
    plt.plot(X3[1:], 1 - f3,label="queue3")
    plt.semilogy()

    plt.xlabel("waiting time")
    plt.ylabel("1-F(X<=x)")

    plt.legend()
    plt.show()


Simulation()


'''
print(A[0])
print(D[0])
print(SIZE[0])
print("----------------")
print(A[1])
print(D[1])
print(SIZE[0])
print("-----------------")
print(A[2])
print(D[2])
print(SIZE[0])
'''
total=0
for i in range(3):
    for j in range(len(Wait[i])):
        total=total+Wait[i][j]
print("wait",total/Total)
averagelen=0
for i in range(3):
    for j in range(len(lenofque[i])):
        averagelen+=lenofque[i][j]
print(averagelen/Total)

PlotGraph(Wait[0],Wait[1],Wait[2])
PlotGraph(lenofque[0],lenofque[1],lenofque[2])