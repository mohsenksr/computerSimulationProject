import numpy as np
import math


class Costumer:
    def __init__(self, priority, arrivalTime, enduranceTime):
        self.priority = priority
        self.arrivalTime = arrivalTime
        self.enduranceTime = enduranceTime

    def queue_arrival(self, time):
        self.queueArrivalTime = time


n, landa, mioo, alpha = map(float, input().split(","))
n = int(n)
operatorMioos = []
servers = [[] for i in range(n)]
idle_servers = []
for i in range(n):
    mioos = [x for x in map(float, input().split(","))]
    idle_servers.append(len(mioos))
    operatorMioos.append(sorted(mioos))

reception_q = [[] for i in range(5)]
queues = [[[] for i in range(5)]for j in range(n)]
costumer_count = 0
costumer_prority_count = [0] * 5
time = 0

wait_time = 0
priority_wait_time = [0] * 5
spent_time = 0
priority_spent_time = [0] * 5
leave_count = 0
reception_q_len = 0
queues_len = [0] * 5

reception_client = None  # the costumer who is geting served
reception_service_time = 0

costumer_limit = 1000000
is_empty = True
while costumer_count < costumer_limit or not is_empty:
    # check for customers endurance in reception queue
    for q in reception_q:
        for costumer in reversed(q):
            if time - costumer.arrivalTime > costumer.enduranceTime:
                spent_time += time - costumer.arrivalTime
                priority_spent_time[costumer.priority] += time - costumer.arrivalTime
                wait_time += time - costumer.arrivalTime
                priority_wait_time[costumer.priority] += time - costumer.arrivalTime
                leave_count += 1
                q.remove(costumer)

    # check for customers endurance in main queues
    for i in queues:
        for q in i:
            for costumer in reversed(q):
                if time - costumer.arrivalTime > costumer.enduranceTime:
                    spent_time += time - costumer.arrivalTime
                    priority_spent_time[costumer.priority] += time - costumer.arrivalTime
                    wait_time += time - costumer.arrivalTime
                    priority_wait_time[costumer.priority] += time - costumer.arrivalTime
                    leave_count += 1
                    q.remove(costumer)

    # check for customers endurance in servers
    for i in servers:
        for costumer in reversed(i):
            if time - costumer[1].arrivalTime > costumer[1].enduranceTime:
                spent_time += time - costumer[1].arrivalTime
                priority_spent_time[costumer[1].priority] += time - costumer[1].arrivalTime
                leave_count += 1
                i.remove(costumer)

    # check for customers endurance in reception
    if reception_client != None and time - reception_client.arrivalTime > reception_client.enduranceTime:
        spent_time += time - reception_client.arrivalTime
        priority_spent_time[reception_client.priority] += time - reception_client.arrivalTime
        leave_count += 1
        reception_client = None

    # Arrivals :
    # customers arrival at that time
    if costumer_count < costumer_limit:
        quantity = np.random.poisson(landa)
        a = costumer_limit - costumer_count
        if a < quantity:
            quantity = a
        costumer_count += quantity
        for i in range(quantity):
            priority = np.random.uniform()  # for customer priority
            # amount of time that costumer get tired
            endurance = np.random.exponential(alpha)
            if priority <= 0.5:
                reception_q[0].append(Costumer(0, time, endurance))
                costumer_prority_count[0] += 1
            elif priority <= 0.7:
                reception_q[1].append(Costumer(1, time, endurance))
                costumer_prority_count[1] += 1
            elif priority <= 0.85:
                reception_q[2].append(Costumer(2, time, endurance))
                costumer_prority_count[2] += 1
            elif priority <= 0.95:
                reception_q[3].append(Costumer(3, time, endurance))
                costumer_prority_count[3] += 1
            else:
                reception_q[4].append(Costumer(4, time, endurance))
                costumer_prority_count[4] += 1

    # reception service:
    if reception_client != None:
        reception_service_time -= 1
        if reception_service_time == 0:
            q = np.random.uniform()          # choose queue number
            reception_client.queue_arrival(time)
            queues[int(q // (1/n))][reception_client.priority].append(reception_client)
            reception_client = None

    # move from reception_q to reception server
    if reception_client == None:
        for i in reversed(range(5)):
            if len(reception_q[i]) > 0:
                reception_service_time = math.ceil(np.random.exponential(1/mioo))  # next service time
                reception_client = reception_q[i].pop(0)
                wait_time += time - reception_client.arrivalTime
                priority_wait_time[reception_client.priority] += time - reception_client.arrivalTime
                break

    # queues service :
    for i in range(n):
        if len(servers[i]) > 0:
            for j in reversed(range(len(servers[i]))):
                servers[i][j][0] -= 1
                if servers[i][j][0] == 0:
                    costumer = servers[i].pop(j)[1]
                    spent_time += time - costumer.arrivalTime
                    priority_spent_time[costumer.priority] += time - costumer.arrivalTime
                    idle_servers[i] += 1

    # move from queues to servers
    for i in range(n):
        if idle_servers[i] > 0:
            for k in reversed(range(5)):
                if len(queues[i][k]) > 0:
                    idle_servers[i] -= 1
                    service_time = math.ceil(np.random.exponential(1/operatorMioos[i][idle_servers[i]]))
                    costumer = queues[i][k].pop(0)
                    wait_time += time - costumer.queueArrivalTime
                    priority_wait_time[costumer.priority] += time - costumer.queueArrivalTime
                    servers[i].append([service_time, costumer])
                    if idle_servers[i] == 0:
                        break

    # check if system is empty
    for q in reception_q:
        if len(q) > 0:
            is_empty = False
            break
    else:
        if reception_client != None:
            is_empty = False
        else:
            for p in queues:
                for q in p:
                    if len(q) > 0:
                        is_empty = False
                        break
                else:
                    continue
                break
            else:
                for p in servers:
                    if len(p) > 0:
                        is_empty = False
                        break
                else:
                    is_empty = True

    reception_q_len += sum([len(x) for x in reception_q])
    for i in range(n):
        queues_len[i] += sum([len(x) for x in queues[i]])
    time += 1

print('Costumer count:\t', costumer_count)
print('Tired costumer count:\t', leave_count)
print('Avarage waiting time in queues:\t', wait_time / costumer_count)
for i in range(5):
    print('\tAvarage waiting in queues of',i,'priority costomers:\t', priority_wait_time[i] / costumer_prority_count[i])
print('Avarage spent time in the system:\t', spent_time / costumer_count)
for i in range(5):
    print('\tAvarage spent time in the system of',i,'priority costomers:\t', priority_spent_time[i] / costumer_prority_count[i])
print('Avarage reception queue length:\t', reception_q_len / time)
for i in range(n):
    print('\tAvarage queue',i,'length:\t', queues_len[i] / time)
