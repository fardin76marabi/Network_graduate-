import random
import matplotlib.pyplot as plt
import numpy as np

flow_random_buffer=[]
pkt_random_buffer=[]
ecmp_random_buffer=[]
size_buffer=[]

maxBufferSize=24

class Packet:
  def __init__(self, id,flowId,start):
    self.id=id
    self.flowId=flowId
    self.strat=start
    self.end=0
    self.current=0
    self.routeRandom=[]
    self.routeECMP=[]
    self.routeR=[]
    self.dst=0
  def nextRouteRandom(self):
    if len(self.routeRandom)==0:
      return 0
    return self.routeRandom[0]   ###Check here
  def nextRouteR(self):
    if len(self.routeR)==0:
      return 0                          
    return self.routeR[0]
  def nextEcmp(self):
    if len(self.routeECMP)==0:
      return 0
    return self.routeECMP[0]



class Flow:
  def __init__(self, id,type):
    self.routeECMP=[]
    self.routeRandom=[]
    self.id=id
    self.packetList=[]
    self.type=type
    self.start=0
    self.end=0
    self.dst=0
    self.sentList=[]
  def create_packets(self,num):
    for i in range(num):
      self.packetList.append(Packet(i,self.id,self.start))



class Server:
  def __init__(self, name):
    self.name = name
    #self.ip = ip
    self.dst=0
    self.flowList=[]
    self.upperLink=[]
    self.sentList=[]
    self.routeRandom=[]
    self.routeECMP=[]
  def have_space(self):
    return True
  def create_flows(self):
    numOfFlow=random.randint(5, 15)##change to (5, 15)
    idOfIt=int((self.name)[-1])
    idOfIt2=(self.name)[-2]
    if idOfIt2.isdigit()==True:           #####CHECK HERE
      idOfIt=int(idOfIt2)*10+idOfIt
    destination=random.randint(0, 15)#change to (0, 15)
    if destination == idOfIt:
       destination=(destination+1)%15#check here
    for i in range(numOfFlow):
      if((random.randint(0, 100))<=80):
        type="mouse"
        numOfPkt=random.randint(1, 10) ##change to (2, 20)
      else:
        type="elephant"
        numOfPkt=random.randint(10, 25) ##change to (500, 1000)
      self.flowList.append(Flow(i,type))
      self.flowList[i].dst="User"+str(destination)
      self.flowList[i].create_packets(numOfPkt)
    
    


class Switch:
  def __init__(self, name):
    self.name = name
    #self.ip = ip
    self.maxBuffer=maxBufferSize
    self.bufferList=[]
    self.upperLink=[]
    self.lowerLink=[]
    self.users=[]
  def have_space(self):
    if len(self.bufferList) < maxBufferSize:
      return True
    else:
      return False
  
  

def create_users(num):
    listofusers=[]
    for x in range(num):
         listofusers.append(Server("User"+str(x)) )
    return listofusers

def create_switch(num,name):
    listofedges=[]
    for x in range(num):
         listofedges.append(Switch(name+str(x)) )
    return listofedges

def create_user_connections(edgeList,userList):
    i=0
    for x in edgeList:
        x.lowerLink.append(userList[2*i])
        x.lowerLink.append(userList[2*i+1])
        (userList[2*i].upperLink).append(x)
        (userList[2*i+1].upperLink).append(x)
        x.users.append(userList[2*i])
        x.users.append(userList[2*i+1])
        i=i+1

def create_edge_connections(aggList,edgeList):
    for i in range(len(aggList)):
        if(i%2 ==0):
          (aggList[i].lowerLink).append(edgeList[i])
          (aggList[i].lowerLink).append(edgeList[i+1])
          (edgeList[i].upperLink).append(aggList[i])
          (edgeList[i+1].upperLink).append(aggList[i])
          aggList[i].users=aggList[i].users+edgeList[i+1].users
        else:
          (aggList[i].lowerLink).append(edgeList[i])
          (aggList[i].lowerLink).append(edgeList[i-1])
          (edgeList[i].upperLink).append(aggList[i])
          (edgeList[i-1].upperLink).append(aggList[i])
          aggList[i].users=aggList[i].users+edgeList[i-1].users
        aggList[i].users=aggList[i].users+edgeList[i].users

def create_Agg_connections(coreList,aggList):
    length=len(coreList)
    for i in range(length):
      if(i<length/2):
        for j in range(len(aggList)):
          if(j%2==0):
            (coreList[i].lowerLink).append(aggList[j])
            (aggList[j].upperLink).append(coreList[i])
      else:
        for j in range(len(aggList)):
          if(j%2!=0):
            (coreList[i].lowerLink).append(aggList[j])
            (aggList[j].upperLink).append(coreList[i])



def Rest(routeList,DST):##changing here
  dst=listOfUsers[0]
  for k in listOfUsers:
    if k.name==DST:
      dst=k
  if len(routeList)==1:
    routeList.append(dst)
  elif len(routeList)==2:
    routeList.append(dst.upperLink[0])
    routeList.append(dst)
  else:
    for k in listOfCores:
      if k==routeList[-1]:
        Core=k
    for k in Core.lowerLink :
      for j in k.users:
        if dst==j:##We change in here
          routeList.append(k)
    routeList.append(dst.upperLink[0])
    routeList.append(dst)


def create_Links(users,edges,aggs,cores):
  return [[0 for x in range(users+edges+aggs+cores)] for y in range(users+edges+aggs+cores)]

def findindex(str):
  firstCh=str[0]
  lastCh=int(str[-1])
  lastCh2=(str[-2])
  if lastCh2.isdigit()==True:
    lastCh=int(lastCh2)*10+lastCh 
  ind=0
  match firstCh:
    case 'U':
      ind=lastCh
    case 'E':
      ind=16+lastCh
    case 'A':
      ind=16+8+lastCh
    case 'C':
      ind=16+8+8+lastCh
  return ind

def check_end():
  for user in listOfUsers:
    for flow in user.flowList:
      if len(flow.packetList) != len(flow.sentList): 
        return False
  return True




def routeFlowRandom():
  for i in listOfUsers:
    for flow in i.flowList:
      done=False
      dst=i.flowList[0].dst
      up=(i.upperLink).copy()
      while True:
        rand=random.randint(0,len(up)-1)
        chosen=up[rand]
        for k in chosen.users:
          if dst==k.name:
            flow.routeRandom.append(chosen)
            done=True
        if done==True:
          routeBack=Rest(flow.routeRandom,dst)
          break
        up.clear()
        up=(chosen.upperLink).copy()
        flow.routeRandom.append(chosen)
        if(chosen.name[0]=="C"):
          routeBack=Rest(flow.routeRandom,dst)#mybe this is extra
          break



def routeRandomPacket():
  for user in listOfUsers:
    for flow in user.flowList:
      for pkt in flow.packetList:
        done=False
        dst=user.flowList[0].dst
        up=(user.upperLink).copy()
        while True:
          rand=random.randint(0,len(up)-1)
          chosen=up[rand]
          for k in chosen.users:
            if dst==k.name:
              pkt.routeR.append(chosen)
              done=True
          if done==True:
            routeBack=Rest(pkt.routeR,dst)
            break
          up.clear()
          up=(chosen.upperLink).copy()
          pkt.routeR.append(chosen)
          if(chosen.name[0]=="C"):
            routeBack=Rest(pkt.routeR,dst)
            break

def routeEcmp():
  for user in listOfUsers:
    src=user
    DST=user.flowList[0].dst
    dst=user.flowList[0]
    for k in listOfUsers:
      if k.name==DST:
        dst=k
    i=0
    for flow in user.flowList: 
      if dst.upperLink==src.upperLink:
        flow.routeECMP.append(user.upperLink[0])
      elif (dst.upperLink[0]).upperLink==(src.upperLink[0]).upperLink:
        total=[]
        route0=[]
        route0.append(src.upperLink[0])
        route0.append((src.upperLink[0]).upperLink[0])
        total.append(route0)
        route1=[]
        route1.append(src.upperLink[0])
        route1.append((src.upperLink[0]).upperLink[1])
        total.append(route1)
        flow.routeECMP.extend(total[i%2])
      else :
        total=[]
        route0=[]
        route0.append(src.upperLink[0])
        route0.append((src.upperLink[0]).upperLink[0])
        route0.append(((src.upperLink[0]).upperLink[0]).upperLink[0])
        total.append(route0)
        route1=[]
        route1.append(src.upperLink[0])
        route1.append((src.upperLink[0]).upperLink[0])
        route1.append(((src.upperLink[0]).upperLink[0]).upperLink[1])
        total.append(route1)
        route2=[]
        route2.append(src.upperLink[0])
        route2.append((src.upperLink[0]).upperLink[1])
        route2.append(((src.upperLink[0]).upperLink[1]).upperLink[0])
        total.append(route2)
        route3=[]
        route3.append(src.upperLink[0])
        route3.append((src.upperLink[0]).upperLink[1])
        route3.append(((src.upperLink[0]).upperLink[1]).upperLink[1])
        total.append(route3)
        flow.routeECMP.extend(total[i%4])
      Rest(flow.routeECMP,DST)
      i=i+1
      

def send_flow_random():
  Done=[]
  time=0
  print("Waiting send_flow_random...")
  while True:
    matrix=create_Links(len(listOfUsers),len(listOfEdges),len(listOfAggs),len(listOfCores))
    time=time+1
    if check_end():
      break
    for user in listOfUsers:
      flowCheck=0
      for flow in user.flowList:
        if len(flow.packetList)!=len(flow.sentList): #len(flow.packetList)!=0
          for pkt in flow.packetList:
            if pkt.current.name==pkt.dst:# pkt arrived to dst
              if pkt not in flow.sentList:
                flow.sentList.append(pkt)
                pkt.end=time
                if time>= flow.end:
                  flow.end=time
                continue
              else:#print("Already added to sent list")
                continue 
            current=findindex(pkt.current.name)
            if pkt.nextRouteRandom()==0:
              continue
            next=findindex(pkt.nextRouteRandom().name)
            if (matrix [current][next]==0) & (matrix [next][current] ==0) &((pkt.nextRouteRandom()).have_space()==True):#link between next and current is free
              pkt.current=pkt.nextRouteRandom()
              if pkt.current.name!=pkt.dst:#if next is not dst 
                pkt.current.bufferList.append(pkt)
              matrix [current][next]=1
              matrix [next][current]=1
              if len(pkt.routeRandom) >0:
                del[pkt.routeRandom[0]]
              continue
            else:#if link between current and next be busy
              continue
        else:#if the flow does not have any pkt
          if flow not in Done:
            Done.append(flow)
          continue
    for switch in (listOfEdges+listOfAggs+listOfCores):
      if len(switch.bufferList)!=0:
        switch.bufferList.pop(-1)
  print("Done")
  totalFCTelf=0
  numOfElf=0
  totalFCTmou=0
  numOfmou=0
  for user in listOfUsers:
    for flow in user.flowList:
      if flow.type=="mouse":
        numOfmou=numOfmou+1
        totalFCTmou=totalFCTmou+int(flow.end)
      else:
        numOfElf=numOfElf+1
        totalFCTelf=totalFCTelf+int(flow.end)
  print("Finish time is ",time)
  print("Average of Mouse is ",totalFCTmou/numOfmou)
  print("Average of Elephant is ",totalFCTelf/numOfElf)
  total=(totalFCTmou+totalFCTelf)/(numOfmou+numOfElf)
  print("Total Average is ",total)
  return total

def send_packet_random():
  Done=[]
  time=0
  print("Waiting send_packet_random...")
  while True:
    matrix=create_Links(len(listOfUsers),len(listOfEdges),len(listOfAggs),len(listOfCores))
    time=time+1
    if check_end():
      break
    for user in listOfUsers:
      flowCheck=0
      for flow in user.flowList:
        if len(flow.packetList)!=len(flow.sentList): #len(flow.packetList)!=0
          for pkt in flow.packetList:
            if pkt.current.name==pkt.dst:# pkt arrived to dst
              if pkt not in flow.sentList:
                flow.sentList.append(pkt)
                pkt.end=time
                if time>= flow.end:
                  flow.end=time
                continue
              else:#print("Already added to sent list")
                continue 
            current=findindex(pkt.current.name)
            if pkt.nextRouteR()==0:
              continue
            next=findindex(pkt.nextRouteR().name)
            if (matrix [current][next]==0) & (matrix [next][current] ==0) & ((pkt.nextRouteR()).have_space()==True):#link between next and current is free
              pkt.current=pkt.nextRouteR()
              if pkt.current.name!=pkt.dst:#if next is not dst 
                pkt.current.bufferList.append(pkt)
              matrix [current][next]=1
              matrix [next][current]=1
              if len(pkt.routeR) >0:
                del[pkt.routeR[0]]
              continue
            else:#if link between current and next be busy
              continue
        else:#if the flow does not have any pkt
          if flow not in Done:
            Done.append(flow)
          continue
    for switch in (listOfEdges+listOfAggs+listOfCores):
      if len(switch.bufferList)!=0:
        switch.bufferList.pop(-1)
  print("Done")
  totalFCTelf=0
  numOfElf=0
  totalFCTmou=0
  numOfmou=0
  for user in listOfUsers:
    for flow in user.flowList:
      if flow.type=="mouse":
        numOfmou=numOfmou+1
        totalFCTmou=totalFCTmou+int(flow.end)
      else:
        numOfElf=numOfElf+1
        totalFCTelf=totalFCTelf+int(flow.end)
  print("Finish time is ",time)
  print("Average of Mouse is ",totalFCTmou/numOfmou)
  print("Average of Elephant is ",totalFCTelf/numOfElf)
  total=(totalFCTmou+totalFCTelf)/(numOfmou+numOfElf)
  print("Total Average is ",total)
  return total             


def send_flow_Ecmp():
  Done=[]
  time=0
  print("Waiting send_flow_Ecmp...")
  while True:
    matrix=create_Links(len(listOfUsers),len(listOfEdges),len(listOfAggs),len(listOfCores))
    time=time+1
    if check_end():
      break
    for user in listOfUsers:
      flowCheck=0
      for flow in user.flowList:
        if len(flow.packetList)!=len(flow.sentList): #len(flow.packetList)!=0
          for pkt in flow.packetList:
            if pkt.current.name==pkt.dst:
              if pkt not in flow.sentList:  
                flow.sentList.append(pkt)
                pkt.end=time
                if time>= flow.end:
                  flow.end=time
                continue
              else:
                continue
            current=findindex(pkt.current.name)
            if pkt.nextEcmp()==0:
              continue
            next=findindex(pkt.nextEcmp().name)#^^^^^^
            if (matrix [current][next]==0) & (matrix [next][current] ==0) & ((pkt.nextEcmp()).have_space()==True):#link between next and current is free
              pkt.current=pkt.nextEcmp()
              if pkt.current.name!=pkt.dst:
                pkt.current.bufferList.append(pkt)
              matrix [current][next]=1
              matrix [next][current]=1
              if len(pkt.routeECMP) >0:
                del[pkt.routeECMP[0]]
              continue
            else:
              continue
        else:
          if flow not in Done:
            Done.append(flow)
          continue
    for switch in (listOfEdges+listOfAggs+listOfCores):
      if len(switch.bufferList)!=0:
        switch.bufferList.pop(-1)
  print("Done")
  totalFCTelf=0
  numOfElf=0
  totalFCTmou=0
  numOfmou=0
  for user in listOfUsers:
    for flow in user.flowList:
      if flow.type=="mouse":
        numOfmou=numOfmou+1
        totalFCTmou=totalFCTmou+int(flow.end)
      else:
        numOfElf=numOfElf+1
        totalFCTelf=totalFCTelf+int(flow.end)
  print("Finish time is ",time)
  print("Average of Mouse is ",totalFCTmou/numOfmou)
  print("Average of Elephant is ",totalFCTelf/numOfElf)
  total=(totalFCTmou+totalFCTelf)/(numOfmou+numOfElf)
  print("Total Average is ",total)
  return total


def create_route_dst_for_pkts(listOfUsers):
  for user in listOfUsers:
    for flow in user.flowList:
      flow.sentList=[]
      for pkt in flow.packetList:
        #pkt.routeRandom=user.routeRandom.copy() 
        pkt.routeRandom=flow.routeRandom.copy() ##newly added instead of above
        pkt.routeECMP=flow.routeECMP.copy() ###compy is added after 
        pkt.dst=flow.dst
        pkt.current=user

def change_bufferSize(num):
    for switch in (listOfEdges+listOfAggs+listOfCores):
        switch.maxBuffer=num

def draw_chart():
    # line 1 points
    x1 = np.array(size_buffer)
    y1 = np.array(flow_random_buffer)
    # plotting the line 1 points
    plt.plot(x1, y1, label = "flow_random")

    # line 2 points
    x2 = np.array(size_buffer)
    y2 = np.array(pkt_random_buffer)
    # plotting the line 2 points
    plt.plot(x2, y2, label = "pkt_random")

    # line 3 points
    x3 = np.array(size_buffer)
    y3 = np.array(ecmp_random_buffer)
    # plotting the line 3 points
    plt.plot(x3, y3, label = "ecmp_random")

    # naming the x axis
    plt.xlabel('Size Of Buffer')
    # naming the y axis
    plt.ylabel('Average FCT Time ')
    # giving a title to my graph
    #plt.title('Average Number Of Tasks Meeting Deadlines.')

    # show a legend on the plot
    plt.legend()

    # function to show the plot
    plt.show()    
def Normalize():
    for user in listOfUsers:
        user.sentList=[]
        user.routeRandom=[]
        user.routeECMP=[] 
        for flow in user.flowList:
            flow.routeECMP=[]
            flow.routeRandom=[]
            flow.end=0
            flow.sentList=[]
            for pkt in flow.packetList:
                pkt.end=0
                pkt.current=0
                pkt.routeRandom=[]
                pkt.routeECMP=[]
                pkt.routeR=[]

numOfUsers=16
numOfEdges=int(numOfUsers/2)
numOfAggs=numOfEdges
numOfCores=int(numOfEdges/2)

Links=create_Links(numOfUsers,numOfEdges,numOfAggs,numOfCores)

listOfUsers=create_users(numOfUsers)
listOfEdges=create_switch(numOfEdges,"Edge")
listOfAggs=create_switch(numOfEdges,"Agg")
listOfCores=create_switch(numOfCores,"Core")


create_user_connections(listOfEdges,listOfUsers)

create_edge_connections(listOfAggs,listOfEdges)

create_Agg_connections(listOfCores,listOfAggs)


for i in listOfUsers:
  i.create_flows()


i=0
iteration=10
maxBufferSize=10
buffSize=maxBufferSize

while(i<iteration):
    print("MaxBufferSize is ",buffSize)
    size_buffer.append(buffSize)
    #
    routeFlowRandom() ##the first one is routeFlowRandom2 ,it is its subtitution
    create_route_dst_for_pkts(listOfUsers)
    total=send_flow_random()
    flow_random_buffer.append(total)
    print("\n")
    #
    routeEcmp()
    create_route_dst_for_pkts(listOfUsers)
    total=send_flow_Ecmp()
    ecmp_random_buffer.append(total)
    print("\n")
    #
    create_route_dst_for_pkts(listOfUsers)
    routeRandomPacket()
    total=send_packet_random()
    pkt_random_buffer.append(total)
    print("\n")
    #
    Normalize()
    change_bufferSize(int(buffSize))
    buffSize*=1.4
    i+=1

draw_chart()