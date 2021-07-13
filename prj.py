import numpy as np
import matplotlib.pyplot as plt
import math


class Customer:
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
customer_count = 0
customer_prority_count = [0] * 5
time = 0


wait_time = 0
priority_wait_time = [0] * 5
spent_time = 0
priority_spent_time = [0] * 5
leave_count = 0
reception_q_len = 0
queues_len = [0] * n

times = [0]
customers_in_system_array = [0]
reception_q_lens_array = [0]
queues_lens_array = [[0] for i in range(5)]

reception_client = None  # the customer who is geting served
reception_service_time = 0

customer_limit = 100000
is_empty = True
while customer_count < customer_limit or not is_empty:
    # check for customers endurance in reception queue
    for q in reception_q:
        for customer in reversed(q):
            if time - customer.arrivalTime > customer.enduranceTime:
                spent_time += time - customer.arrivalTime
                priority_spent_time[customer.priority] += time - \
                    customer.arrivalTime
                wait_time += time - customer.arrivalTime
                priority_wait_time[customer.priority] += time - \
                    customer.arrivalTime
                leave_count += 1
                q.remove(customer)

    # check for customers endurance in main queues
    for i in queues:
        for q in i:
            for customer in reversed(q):
                if time - customer.arrivalTime > customer.enduranceTime:
                    spent_time += time - customer.arrivalTime
                    priority_spent_time[customer.priority] += time - \
                        customer.arrivalTime
                    wait_time += time - customer.queueArrivalTime
                    priority_wait_time[customer.priority] += time - \
                        customer.queueArrivalTime
                    leave_count += 1
                    q.remove(customer)

    # check for customers endurance in servers
    for i in servers:
        for customer in reversed(i):
            if time - customer[1].arrivalTime > customer[1].enduranceTime:
                spent_time += time - customer[1].arrivalTime
                priority_spent_time[customer[1].priority] += time - \
                    customer[1].arrivalTime
                leave_count += 1
                idle_servers[servers.index(i)] += 1
                i.remove(customer)

    # check for customers endurance in reception
    if reception_client != None and time - reception_client.arrivalTime > reception_client.enduranceTime:
        spent_time += time - reception_client.arrivalTime
        priority_spent_time[reception_client.priority] += time - \
            reception_client.arrivalTime
        leave_count += 1
        reception_client = None

    # Arrivals :
    # customers arrival at that time
    if customer_count < customer_limit:
        quantity = np.random.poisson(landa)
        a = customer_limit - customer_count
        if a < quantity:
            quantity = a
        customer_count += quantity
        for i in range(quantity):
            priority = np.random.uniform()  # for customer priority
            # amount of time that customer get tired
            endurance = np.random.exponential(alpha)
            if priority <= 0.5:
                reception_q[0].append(Customer(0, time, endurance))
                customer_prority_count[0] += 1
            elif priority <= 0.7:
                reception_q[1].append(Customer(1, time, endurance))
                customer_prority_count[1] += 1
            elif priority <= 0.85:
                reception_q[2].append(Customer(2, time, endurance))
                customer_prority_count[2] += 1
            elif priority <= 0.95:
                reception_q[3].append(Customer(3, time, endurance))
                customer_prority_count[3] += 1
            else:
                reception_q[4].append(Customer(4, time, endurance))
                customer_prority_count[4] += 1

    # reception service:
    if reception_client != None:
        reception_service_time -= 1
        if reception_service_time == 0:
            q = np.random.uniform()          # choose queue number
            reception_client.queue_arrival(time)
            queues[int(q // (1/n))
                   ][reception_client.priority].append(reception_client)
            reception_client = None

    # move from reception_q to reception server
    if reception_client == None:
        for i in reversed(range(5)):
            if len(reception_q[i]) > 0:
                reception_service_time = math.ceil(
                    np.random.exponential(1/mioo))  # next service time

                reception_client = reception_q[i].pop(0)
                wait_time += time - reception_client.arrivalTime
                priority_wait_time[reception_client.priority] += time - \
                    reception_client.arrivalTime
                break

    # queues service :
    for i in range(n):
        if len(servers[i]) > 0:
            for j in reversed(range(len(servers[i]))):
                servers[i][j][0] -= 1
                if servers[i][j][0] == 0:
                    customer = servers[i].pop(j)[1]
                    spent_time += time - customer.arrivalTime
                    priority_spent_time[customer.priority] += time - \
                        customer.arrivalTime
                    idle_servers[i] += 1

    # move from queues to servers
    for i in range(n):
        if idle_servers[i] > 0:
            for k in reversed(range(5)):
                if len(queues[i][k]) > 0:
                    idle_servers[i] -= 1
                    service_time = math.ceil(np.random.exponential(
                        1/operatorMioos[i][idle_servers[i]]))
                    customer = queues[i][k].pop(0)
                    wait_time += time - customer.queueArrivalTime
                    priority_wait_time[customer.priority] += time - \
                        customer.queueArrivalTime
                    servers[i].append([service_time, customer])
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

    temp_reception_q_len = sum([len(x) for x in reception_q])
    reception_q_len += temp_reception_q_len
    reception_q_lens_array.append(temp_reception_q_len)
    comulative_queues_count = temp_reception_q_len
    for i in range(n):
        q_len = sum([len(x) for x in queues[i]])
        comulative_queues_count += q_len
        queues_len[i] += q_len
        queues_lens_array[i].append(q_len)

    times.append(time)
    customer_in_system = comulative_queues_count + \
        sum([len(x) for x in servers])
    if(reception_client != None):
        customer_in_system += 1
    customers_in_system_array.append(customer_in_system)

    time += 1


print('customer count:\t', customer_count)
print('Tired customer count:\t', leave_count)
print('Avarage waiting time in queues:\t', wait_time / customer_count)
for i in range(5):
    print('\tAvarage waiting in queues of', i, 'priority costomers:\t',
          priority_wait_time[i] / customer_prority_count[i])
print('Avarage spent time in the system:\t', spent_time / customer_count)
for i in range(5):
    print('\tAvarage spent time in the system of', i, 'priority costomers:\t',
          priority_spent_time[i] / customer_prority_count[i])
print('Avarage reception queue length:\t', reception_q_len / time)
for i in range(n):
    print('\tAvarage queue', i, 'length:\t', queues_len[i] / time)


x = times
y = reception_q_lens_array
plt.plot(x, y, label="reception queue")

plt.xlabel('time')
plt.ylabel('number')
plt.title('length of queues in time')
plt.legend()
plt.show()


for i in range(n):
    plt.plot(x, queues_lens_array[i], label="queue number " + str(i))
    plt.xlabel('time')
    plt.ylabel('number')
    plt.title('length of queues in time')
    plt.legend()
    plt.show()

y = customers_in_system_array
plt.plot(x, y, label="customers in system")

plt.xlabel('time')
plt.ylabel('number')
plt.title('customers in system in time')
plt.legend()
plt.show()
