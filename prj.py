import numpy as np
import math

class Costumer:
    def __init__(self, priority, arrivalTime, enduranceTime):
        self.priority = priority
        self.arrivalTime = arrivalTime
        self.enduranceTime = enduranceTime

    def __str__(self):
        return str(self.priority) + '\t' + str(self.arrivalTime)

n, landa, mioo, alpha = map(float, input().split(","))
n = int(n)
operatorMioos = []
servers = [[] for i in range(n)]
idle_servers = []
for i in range(n):
    mioos = [float(i) for i in input().split(',')]
    idle_servers.append(len(mioos))
    operatorMioos.append(sorted(mioos))

reception_q = [[] for i in range(5)]
queues = [[[] for i in range(5)]for j in range(n)]
customer_count = 0
time = 0

wait_time = 0
priority_wait_time = [0] * 5
spent_time = 0
priority_spent_time = [0] * 5
leave_count = 0
reception_q_len = 0
queues_len = [0] * 5

reception_client = None  # the costomer who is geting served
reception_service_time = 0

customer_limit = 1000000

while customer_count <= customer_limit:

    # Arrivals :
    # customers arrival at that time
    a = np.random.poisson(landa)
    customer_count += a
    for i in range(a):
        r = np.random.uniform()  # for customer priority
        w = np.random.exponential(alpha)  # amount of time that costumer get tired
        if r <= 0.5:
            reception_q[0].append(Costumer(0,time, w))
        elif r <= 0.7:
            reception_q[1].append(Costumer(1,time, w))
        elif r <= 0.85:
            reception_q[2].append(Costumer(2,time, w))
        elif r <= 0.95:
            reception_q[3].append(Costumer(3,time, w))
        else:
            reception_q[4].append(Costumer(4,time, w))

    # reception service:
    if reception_client != None:
        reception_service_time -= 1
        if reception_service_time == 0:
            r = np.random.uniform()
            queues[int(r // (1/n))][reception_client.priority].append(reception_client)
            reception_client = None
    if reception_client == None:
        for i in reversed(range(5)):
            if len(reception_q[i]) > 0:
                reception_service_time = math.ceil(np.random.exponential(1/mioo))  # next service time
                reception_client = reception_q[i].pop(0)
                break

    # queues service :
    for i in range(n):
        if len(servers[i]) > 0:
            for j in reversed(range(len(servers[i]))):
                servers[i][j][0] -= 1
                if servers[i][j][0] == 0:
                    servers[i].pop(j)
                    idle_servers[i] += 1

    for i in range(n):
        if idle_servers[i] > 0:
            for k in reversed(range(5)):
                if len(queues[i][k]) > 0:
                    idle_servers[i] -= 1
                    service_time = math.ceil(np.random.exponential(1/operatorMioos[i][idle_servers[i]]))
                    servers[i].append((service_time, time, queues[i][k].pop(0)))
                    if idle_servers[i] == 0:
                        break

    time += 1
