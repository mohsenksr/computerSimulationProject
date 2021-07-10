import numpy as np
import math

n, landa, mioo, alpha = map(float, input().split(","))
n = int(n)
operatorMioos = []
servers = [[]] * n
idle_servers = []
for i in range(n):
    mioos = ([float(i) for i in input().split(',')]
    idle_servers.append(len(mioos))
    operatorMioos.append(sorted(mioos))

reception_q = [[]] * 5
queues = [[[]] * 5] * n
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

customer_limit = 10000000

while customer_count <= customer_limit:

    # Arrivals :
    # customers arrival at that time
    a = np.random.poisson(landa)
    customer_count += a
    for i in range(a):
        r = np.random.uniform()  # for customer priority
        w = np.random.exponential(alpha)  # amount of time that costumer get tired
        c =  Customer(4,time, w)  # new costumer
        if r <= 0.5:
            c.priority = 0
            reception_q[0].append(c)
        elif r <= 0.7:
            c.priority = 1
            reception_q[1].append(c)
        elif r <= 0.85:
            c.priority = 2
            reception_q[2].append(c)
        elif r <= 0.95:
            c.priority = 3
            reception_q[3].append(c)
        else:
            reception_q[4].append(c)

    # reception service:
    if reception_client != None
        reception_service_time -= 1
        if reception_service_time == 0:
            r = np.random.uniform()
            queues[r // (1/n)][reception_client.priority].append(reception_client)
            reception_client = None
    if reception_client == None:
        for i in reversed(range(5)):
            if len(reception_q[i]) > 0:
                reception_service_time = math.ceil(np.random.exponential(1/mioo))  # next service time
                reception_client = reception_q[i].pop(0)
                break

    for i in range(len(servers)):
        if len(servers[i]) > 0:
            for j in range(len(servers[i])):
                servers[i][j][0] -= 1
                if servers[i][j][0] == 0:
                    servers[i].pop(j)
                    idle_servers[i] += 1

    for i in range(len(servers)):
        if idle_servers[i] > 0:
            for k in reversed(range(5)):
                if len(queues[i][k]) > 0:
                    idle_servers[i] -= 1
                    service_time = math.ceil(np.random.exponential(1/operatorMioos[i][idle_servers[i]]))
                    servers[i].append((service_time, time, queues[i][k].pop(0)))
                    if idle_servers[i] == 0:
                        break
        











class Customer:
    def __init__(self, priority, arrivalTime, enduranceTime):
        self.priority = priority
        self.arrivalTime = arrivalTime
        self.enduranceTime = enduranceTime
