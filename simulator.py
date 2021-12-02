from random import random
from math import log
from queue import Queue

INF = 1000000000


class Simulator:
    def __init__(self, mean_interarrival_time, mean_service_time, total_customers):
        self.mean_interarrival_time = mean_interarrival_time
        self.mean_service_time = mean_service_time
        self.total_customers = total_customers

        self.delayed_customers = 0
        self.queue_length = 0
        self.server_busy = False

        self.delay_sum = 0
        self.queue_length_sum = 0
        self.server_busy_sum = 0

        self.time = 0
        self.next_arrival = INF
        self.next_departure = INF

        self.arrival_times = Queue()

        self.interarrival_rv_pairs = []
        self.service_rv_pairs = []

    def random_interarrival_time(self):
        urv = random()
        erv = -self.mean_interarrival_time * log(urv)
        self.interarrival_rv_pairs.append((urv, erv))
        return erv

    def random_service_time(self):
        urv = random()
        erv = -self.mean_service_time * log(urv)
        self.service_rv_pairs.append((urv, erv))
        return erv

    def update_time(self, next_event_time):
        self.queue_length_sum += self.queue_length * (next_event_time - self.time)
        self.server_busy_sum += self.server_busy * (next_event_time - self.time)
        self.time = next_event_time

    def handle_arrival(self):
        self.update_time(self.next_arrival)

        self.next_arrival = self.time + self.random_interarrival_time()
        if self.server_busy:
            self.queue_length += 1
            self.arrival_times.put(self.time)
        else:
            self.delayed_customers += 1
            self.server_busy = True
            self.next_departure = self.time + self.random_service_time()

    def handle_departure(self):
        self.update_time(self.next_departure)

        if self.queue_length == 0:
            self.server_busy = False
            self.next_departure = INF
        else:
            self.queue_length -= 1
            self.delay_sum += self.time - self.arrival_times.get()
            self.delayed_customers += 1
            self.next_departure = self.time + self.random_service_time()

    def run(self):
        self.next_arrival = self.random_interarrival_time()

        while self.delayed_customers < self.total_customers:
            if self.next_arrival < self.next_departure:
                self.handle_arrival()
            else:
                self.handle_departure()

    def get_statistics(self):
        return {
            'average_delay_in_queue': self.delay_sum / self.delayed_customers,
            'average_queue_length': self.queue_length_sum / self.time,
            'server_utilization': self.server_busy_sum / self.time,
            'time_simulation_ended': self.time
        }

    def get_rv_pairs(self):
        return self.interarrival_rv_pairs, self.service_rv_pairs
