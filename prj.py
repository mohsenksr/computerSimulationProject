import numpy as np

n, landa, mioo, alpha = map(float, input().split(","))
n = int(n)
operatorMioos = []

for i in range(n):
    operatorMioos.append(float(input()))

reception_q = [[]]*5
queues = [[[]]*5]*n
customer_count = 0
time = 0


customer_limit = 10

while customer_count <= customer_limit:

    # Arrivals :
    # customers arrival at that time  l for lambda
    a = np.random.poisson(landa)
    customer_count += a
    for i in range(a):
        r = np.random.uniform()  # for customer priority
        if r <= 0.5:
            reception_q[0].append()
        elif r <= 0.7:
            reception_q[1].append()
        elif r <= 0.85:
            reception_q[2].append()
        elif r <= 0.95:
            reception_q[3].append()
        else:
            reception_q[4].append()


class Customer:
    def __init__(self, priority, arrivalTime, enduranceTime):
        self.priority = priority
        self.arrivalTime = arrivalTime
        self.enduranceTime = enduranceTime
