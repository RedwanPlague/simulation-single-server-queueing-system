from simulator import Simulator
import matplotlib.pyplot as plt
from statistics import mean, median
import csv


def write_statistics(f, title, data, beta=None):
    f.write('\n')
    f.write(title + ' time min:    ' + str(min(data)) + '\n')
    f.write(title + ' time max:    ' + str(max(data)) + '\n')
    f.write(title + ' time mean:   ' + str(mean(data)) + '\n')
    f.write(title + ' time median: ' + str(median(data)) + '\n')

    if beta is None:
        bucket_boundaries = [x/10 for x in range(0, 11)]
    else:
        # bucket_boundaries = [0, 0.1, 0.3, 0.7, 1.5, 3.1]
        bucket_boundaries = [0, beta/2, beta, 2*beta, 3*beta]

    weights = [1/len(data)] * len(data)

    plt.hist(data, bins=bucket_boundaries, weights=weights, edgecolor='white')
    plt.ylim(0, 1)
    plt.xticks(bucket_boundaries)
    plt.title(title + ' P(x)')
    plt.show()
    plt.hist(data, bins=bucket_boundaries, cumulative=True, weights=weights, color='green', edgecolor='white')
    plt.ylim(0, 1)
    plt.xticks(bucket_boundaries)
    plt.title(title + ' F(x)')
    plt.show()


def task_a(input_file, output_file):
    with open(input_file, 'r') as f:
        mean_interarrival_time = float(f.readline())
        mean_service_time = float(f.readline())
        total_customers = int(f.readline())

    simulator = Simulator(mean_interarrival_time, mean_service_time, total_customers)
    simulator.run()

    outputs = simulator.get_statistics()
    with open(output_file, 'w') as f:
        f.write('Average delay in queue: ' + str(outputs['average_delay_in_queue']) + ' minutes\n')
        f.write('Average queue length:   ' + str(outputs['average_queue_length']) + '\n')
        f.write('Server utilization:     ' + str(outputs['server_utilization']) + '\n')
        f.write('Time simulation ended:  ' + str(outputs['time_simulation_ended']) + ' minutes\n')
        f.write('\n')

    interarrival_rv_pairs, service_rv_pairs = simulator.get_rv_pairs()

    ix = [urv for urv, erv in interarrival_rv_pairs]
    iy = [erv for urv, erv in interarrival_rv_pairs]
    sx = [urv for urv, erv in service_rv_pairs]
    sy = [erv for urv, erv in service_rv_pairs]

    plt.scatter(ix, iy)
    plt.title('Uni vs Expo - interarrival time')
    plt.show()
    plt.scatter(sx, sy)
    plt.title('Uni vs Expo - service time')
    plt.show()

    with open(output_file, 'a') as f:
        write_statistics(f, 'Uniform', ix + sx)
        write_statistics(f, 'Interarrival', iy, mean_interarrival_time)
        write_statistics(f, 'Service', sy, mean_service_time)


def task_b(input_file, output_file):
    with open(input_file, 'r') as f:
        mean_interarrival_time = float(f.readline())
        f.readline()
        total_customers = int(f.readline())

    table = [[
        'k',
        'Average delay in queue',
        'Average queue length',
        'Server utilization',
        'Time simulation ended'
    ]]

    for k in range(1, 10):
        simulator = Simulator(mean_interarrival_time, mean_interarrival_time * k / 10, total_customers)
        simulator.run()
        outputs = simulator.get_statistics()
        table.append([k / 10] + list(outputs.values()))

    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(table)

    data = table[1:]
    plt.plot([x[0] for x in data], [x[1] for x in data])
    plt.title('Average delay in queue - vs - k')
    plt.show()
    plt.plot([x[0] for x in data], [x[2] for x in data])
    plt.title('Average queue length - vs - k')
    plt.show()
    plt.plot([x[0] for x in data], [x[3] for x in data])
    plt.title('Server utilization - vs - k')
    plt.show()
    plt.plot([x[0] for x in data], [x[4] for x in data])
    plt.title('Time simulation ended - vs - k')
    plt.show()


def main():
    task_a('input.txt', 'output_a.txt')
    # task_b('input.txt', 'output_b.csv')


if __name__ == '__main__':
    main()
