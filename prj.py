import numpy as np
import math

n, landa, mioo, alpha = map(float, input().split(","))
n = int(n)
operatorMioos = []

for i in range(n):
    operatorMioos.append(float(input()))

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
    if reception_client == None:
        reception_service_time = math.ceil(np.random.exponential(1/mioo))  # next service time
    else:
        reception_service_time -= 1
        if reception_service_time == 0:

            //# TODO: add costumer to second queue




class Customer:
    def __init__(self, priority, arrivalTime, enduranceTime):
        self.priority = priority
        self.arrivalTime = arrivalTime
        self.enduranceTime = enduranceTime
