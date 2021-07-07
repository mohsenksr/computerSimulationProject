import numpy as np

n, landa, mioo, alpha = map(float, input().split(","))
n = int(n)
operatorMioos = []

for i in range(n):
    operatorMioos.append(float(input()))

reception_q = [[]]*5
queues = [[[]]*5]*n
costumer_count = 0
time = 0


costumer_limit = 10

while while costumer_count <= costumer_limit:


    # Arrivals :
    a = np.random.poisson(landa) # costumers arrival at that time  l for lambda
    costumer_count += a
    for i in range(a):
        r = np.random.uniform() # for costumer priority
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
