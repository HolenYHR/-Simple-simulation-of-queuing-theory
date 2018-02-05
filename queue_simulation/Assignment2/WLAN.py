import random as rm
import math
import numpy
import matplotlib.pyplot as plt
#站的个数
NUMOFSTATION=5
#waittime=TIMESLOT*RANDOMBACKOF
TIMESLOT=1
#必须要等待的时间间隔
DIFS=2



'''
 ARRIVETIME:the time the packet arrives.
 COLLISIONTIME: the times the collision has occured.
 WAITTIME: the time left to wait
 WINSIZE: the current size of the windows
'''
class Packet:
    def __init__(self,ARRIVETIME,WINSIZE,WAITTIME,SCALE):
        self.ARRIVETIME=ARRIVETIME
        #self.COLLISIONTIME=COLLISIONTIME
        self.WINSIZE=WINSIZE
        self.WAITTIME=WAITTIME
        self.SCALE=SCALE

#包来的时间
A=[[] for q in range(NUMOFSTATION)]
#包传送完的时间
D=[[] for qq in range(NUMOFSTATION)]
#当前包完成的时间
nextFinish=0
#队列的最前面一个包来的时间
ts=[0 for qqq in range(NUMOFSTATION)]
#队列的最后面一个包来的时间
tf=[0 for qqqq in range(NUMOFSTATION)]

#信道是否为空,如果为空则为1否则为0
EMPTY=1
#各个站来包的速率
Lamd=0.8
mu=1

Insystem=[1 for r in range(NUMOFSTATION)]
CouSys=[0 for rr in range(NUMOFSTATION)]

Total=1000000
total=0
WaitTime=[[] for wa in range(NUMOFSTATION)]

IsCollision=False
INF=10000000
UP=10000000
def Simulation():
    global tf,ts,EMPTY,Lamd,nextFinish,D,A,TIMESLOT,DIFS,total,Total,IsCollision,WaitTime
    for i in range(NUMOFSTATION):
        tf[i]=ts[i]=rm.expovariate(Lamd)
        scale=rm.expovariate(mu)
        Win=2
        p=Packet(tf[i],2,tf[i]+DIFS,scale)
        A[i].append(p)
        total=3

    while True:
        min=0
        for i in range(NUMOFSTATION):
            if A[i][CouSys[i]].WAITTIME<A[min][CouSys[min]].WAITTIME:
                min=i

        Same=[]
        IsCollision=False
        for j in range(NUMOFSTATION):
            if j!=min:
                if A[j][CouSys[j]].WAITTIME==A[min][CouSys[min]].WAITTIME:
                    Same.append(j)
                    IsCollision=True
        if IsCollision:
            for station in Same:
                Ws=A[station][CouSys[station]].WINSIZE
                A[station][CouSys[station]].WINSIZE=Ws*2
                Wt=A[station][CouSys[station]].WAITTIME
                A[station][CouSys[station]].WAITTIME=Wt+rm.randint(0,Ws*2)

        else:

            if ts[min]!=UP:
                #如果可以发送的话
                if ts[min]<=nextFinish:
                    virFinish=nextFinish+A[min][CouSys[min]].SCALE
                    for j in range(NUMOFSTATION):
                        if j != min:
                            if A[j][CouSys[j]].ARRIVETIME<virFinish:
                                A[j][CouSys[j]].WAITTIME=virFinish+DIFS+A[min][CouSys[min]].SCALE

                    for s in range(NUMOFSTATION):
                        tt=tf[s]=tf[s]+rm.expovariate(Lamd)
                        while tt<nextFinish and total<Total:
                            scale=rm.expovariate(mu)

                            p=Packet(tt,2,INF,scale)
                            A[s].append(p)
                            tf[s]=tt
                            Insystem[s]+=1
                            total+=1
                            tt+=rm.expovariate(Lamd)

                    D[min].append(nextFinish)
                    wa=nextFinish-A[min][CouSys[min]].ARRIVETIME
                    WaitTime[min].append(wa)
                    nextFinish=virFinish
                    Insystem[min]-=1

                    if Insystem[min]==0 and total<Total:
                        ts[min]=tf[min]=tf[min]+rm.expovariate(Lamd)
                        total+=1
                        scale=rm.expovariate(mu)
                        if ts[min]>nextFinish:
                            p=Packet(ts[min],2,INF,scale)
                        else:
                            p=Packet(ts[min],2,nextFinish+DIFS+rm.randint(0,2),scale)
                        A[min].append(p)
                        Insystem[min]=1
                        CouSys[min]=CouSys[min]+1
                    elif Insystem[min]!=0:
                        CouSys[min]=CouSys[min]+1
                        ts[min]=A[min][CouSys[min]].ARRIVETIME
                        if A[min][CouSys[min]].ARRIVETIME<=nextFinish:
                            wz=A[min][CouSys[min]].WINSIZE
                            A[min][CouSys[min]].WAITTIME=nextFinish+rm.randint(0,wz)
                    else:
                        arr=UP
                        p=Packet(arr,0,0,0)
                        A[min].append(p)
                        ts[min]=UP

                else:
                    nextFinish=ts[min]
            else:
                break

def PlotGraph(array1,array2,array3,array4,array5):
    H1, X1 = numpy.histogram(array1, bins=30, normed=True)
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

    H4, X4 = numpy.histogram(array4, bins=70, normed=True)
    dx = X4[1] - X4[0]
    f4 = numpy.cumsum(H4) * dx
    # X2=numpy.sort(servicetime)
    # f2=numpy.array()
    plt.plot(X4[1:], 1 - f4)
    plt.semilogy()

    H5, X5 = numpy.histogram(array5, bins=70, normed=True)
    dx = X5[1] - X5[0]
    f5 = numpy.cumsum(H5) * dx
    # X2=numpy.sort(servicetime)
    # f2=numpy.array()
    plt.plot(X5[1:], 1 - f5)
    plt.semilogy()
    plt.legend()
    plt.show()


Simulation()

PlotGraph(WaitTime[0],WaitTime[1],WaitTime[2],WaitTime[3],WaitTime[4])

#for i in WaitTime[1]:
  # print(i)