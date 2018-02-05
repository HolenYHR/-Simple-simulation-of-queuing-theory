import random as rm
import matplotlib.pyplot as plt
import numpy
class Packet:
    def __init__(self,arrivetime,virtime,sise):
        self.arrivetime=arrivetime
        self.virtime=virtime
        self.sise=sise
#来的时间
A=[[] for q in range(3)]
#离开时间
D=[[] for qq in range(3)]
#每个队列开头的包的时间
ts=[0 for qqq in range(3)]
#每个队列最后一个包的时间
tf=[0 for qqqq in range(3)]
#各个队列的虚拟时间
virtime=[0  for qqqqq in range(3)]
#系统中总共的包数
conSys=[1 for qqqqqq in range(3)]
#当前的包
conTo=[0 for qqqqqqq in range(3)]
que=[[] for queee in range(3)]

lamd=[20,30,40]
mu=100

Wait=[[] for oo in range(3)]

current=0

total=0
Total=1000000
SIZE=[[] for si in range(3)]
Upbound=10000000
min=0
nextfinish=0



sumocfque=0
number=0
queminsize=0
def Simulation():
    global sumocfque,queminsize,total,current,nextfinish,Upbound,Total,lamd,mu,conTo,conSys,min,number
    for i in range(3):
        tf[i]=ts[i]=(rm.expovariate(lamd[i]))
        scale=rm.expovariate(mu)
        vir=scale+tf[i]
        p=Packet(tf[i],vir,scale)
        A[i].append(p)
        virtime[i]=vir
        SIZE[i].append(scale)
        que[i].append(0)
    total=3
    while True:
        min=0
        for k in range(3):
           # print(len(A[k]),conTo[k])
            if  A[k][conTo[k]].virtime<A[min][conTo[min]].virtime:
                min=k
               # print("k",k,A[k][conTo[k]].arrivetime,A[k][conTo[k]].virtime)

        if ts[min]!=Upbound:
            # print(type(ts[min]),type(nextfinish))
             if ts[min]<=nextfinish:
                 tt = tf[min]=tf[min]+rm.expovariate(lamd[min])
                 while tt<=nextfinish and total<Total:
                     scale=rm.expovariate(mu)
                     vir=max(tt,virtime[min])

                     vir=vir+scale
                     virtime[min] = vir
                     SIZE[min].append(scale)
                     p=Packet(tt,vir,scale)
                     A[min].append(p)
                     conSys[min]+=1
                     que[min].append(conSys[min])
                     tf[min]=tt
                     tttt=rm.expovariate(lamd[min])
                     tt=tt+tttt
                     total+=1
                 D[min].append(nextfinish)

                # if(min==1):

                 #   queminsize+=A[min][conTo[min]].sise

                 #print("num:",number,"que:",min,"Arrive",A[min][conTo[min]].arrivetime,"virtime",A[min][conTo[min]].virtime,"size",A[min][conTo[min]].sise,"nextFinish",nextfinish)
                 wa = nextfinish - A[min][conTo[min]].arrivetime
                 #print("Wait",wa)

                 #print(wa)
                 Wait[min].append(wa)
                 nextfinish=nextfinish+A[min][conTo[min]].sise
                 conSys[min]-=1
                 if conSys[min]==0 and total<=Total:
                     ts[min]=tf[min]=tf[min]+rm.expovariate(lamd[min])
                     total+=1
                     scale=rm.expovariate(mu)
                     vir=max(virtime[min],tf[min])
                     vir=vir+scale
                     virtime[min]=vir
                     p=Packet(ts[min],vir,scale)
                     A[min].append(p)
                     conSys[min]=1
                     conTo[min]=conTo[min]+1
                     que[min].append(0)
                 elif conSys[min]!=0:
                     conTo[min]=conTo[min]+1
                     #print("conTo",conTo[min],"len",len(A[min]))
                     ts[min]=A[min][conTo[min]].arrivetime

                 else:
                     arr=Upbound
                     p=Packet(arr,Upbound,Upbound)
                     A[min].append(p)
                     ts[min]=Upbound

             else:
                 nextfinish=ts[min]

        else:
            break

def PlotGraph(array1,array2,array3):
    H1, X1 = numpy.histogram(array1, bins=70, normed=True)
    dx = X1[1] - X1[0]
    f1 = numpy.cumsum(H1) * dx
    # X2=numpy.sort(servicetime)
    # f2=numpy.array()
    plt.plot(X1[1:], 1 - f1)
    plt.semilogy()

    H2, X2 = numpy.histogram(array2, bins=70, normed=True)
    dx = X2[1] - X2[0]
    f2 = numpy.cumsum(H2) * dx
    # X2=numpy.sort(servicetime)
    # f2=numpy.array()
    plt.plot(X2[1:], 1 - f2)
    plt.semilogy()

    H3, X3 = numpy.histogram(array3, bins=70, normed=True)
    dx = X3[1] - X3[0]
    f3 = numpy.cumsum(H3) * dx
    # X2=numpy.sort(servicetime)
    # f2=numpy.array()
    plt.plot(X3[1:], 1 - f3)
    plt.semilogy()




    plt.legend()
    plt.show()



Simulation()
PlotGraph(Wait[0],Wait[1],Wait[2])
PlotGraph(que[0],que[1],que[2])
#print("-------------")
#print(sumocfque/number)
#for i in range(len(A[1])):
#    print(A[1][i].arrivetime)