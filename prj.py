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
    mioos = map(float, input().split(","))
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
    # check for customers endurance in reception queue
    for i in range(reception_q):
        for j in range(i):
            if(time - j.arrivalTime > j.enduranceTime):
                leave_count += 1
                i.__delitem__(j)

    # check for customers endurance in main queues
    for i in range(queues):
        for j in range(i):
            for k in range(j):
                if(time - k.arrivalTime > k.enduranceTime):
                    leave_count += 1
                    j.__delitem__(k)

    # check for customers endurance in servers
    for i in range(servers):
        for j in range(i):
            if(time - j.arrivalTime > j.enduranceTime):
                leave_count += 1
                i.__delitem__(j)

    # Arrivals :
    # customers arrival at that time
    quantity = np.random.poisson(landa)
    customer_count += quantity
    for i in range(quantity):
        priority = np.random.uniform()  # for customer priority
        # amount of time that costumer get tired
        endurance = np.random.exponential(alpha)
        if priority <= 0.5:
            reception_q[0].append(Costumer(0, time, endurance))
        elif priority <= 0.7:
            reception_q[1].append(Costumer(1, time, endurance))
        elif priority <= 0.85:
            reception_q[2].append(Costumer(2, time, endurance))
        elif priority <= 0.95:
            reception_q[3].append(Costumer(3, time, endurance))
        else:
            reception_q[4].append(Costumer(4, time, endurance))

    # reception service:
    if reception_client != None:
        reception_service_time -= 1
        if reception_service_time == 0:
            priority = np.random.uniform()
            queues[int(priority // (1/n))
                   ][reception_client.priority].append(reception_client)
            reception_client = None
    if reception_client == None:
        for i in reversed(range(5)):
            if len(reception_q[i]) > 0:
                reception_service_time = math.ceil(
                    np.random.exponential(1/mioo))  # next service time
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
                    service_time = math.ceil(np.random.exponential(
                        1/operatorMioos[i][idle_servers[i]]))
                    servers[i].append(
                        (service_time, time, queues[i][k].pop(0)))
                    if idle_servers[i] == 0:
                        break

    time += 1
