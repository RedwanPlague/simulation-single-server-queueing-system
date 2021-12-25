from simulator import Simulator
import matplotlib.pyplot as plt
from statistics import mean, median
import csv


PLOT = True


def write_statistics(title, data, beta=None):
    if beta is None:
        bucket_boundaries = [x / 10 for x in range(0, 11)]
    else:
        # bucket_boundaries = [0, 0.1*beta, 0.3*beta, 0.7*beta, 1.5*beta, 3.1*beta, 6.3*beta]
        # bucket_boundaries = [0, beta / 2, beta, 2 * beta, 3 * beta]
        bucket_boundaries = [x / 10 for x in range(0, int(30*beta))]

    weights = [1 / len(data)] * len(data)

    px, _, _ = plt.hist(data, bins=bucket_boundaries, weights=weights, edgecolor='white')
    # plt.ylim(0, 1)
    # plt.xticks(bucket_boundaries)
    plt.title(title + ' P(x)')
    if PLOT:
        plt.show()
    fx, _, _ = plt.hist(data, bins=bucket_boundaries, cumulative=True, weights=weights, color='green',
                        edgecolor='white')
    # plt.ylim(0, 1)
    # plt.xticks(bucket_boundaries)
    plt.title(title + ' F(x)')
    if PLOT:
        plt.show()

    with open('output_c.txt', 'w' if beta is None else 'a') as f:
        f.write('\n')
        f.write('{} time min:    {:.3f}\n'.format(title, min(data)))
        f.write('{} time max:    {:.3f}\n'.format(title, max(data)))
        f.write('{} time mean:   {:.3f}\n'.format(title, mean(data)))
        f.write('{} time median: {:.3f}\n'.format(title, median(data)))

        f.write('\n')
        f.write('bucket         |  P(x)   |  F(x)\n')
        for i in range(len(bucket_boundaries) - 1):
            f.write('{:.3f} - {:.3f}  |  {:.3f}  |  {:.3f}\n'.format(
                bucket_boundaries[i], bucket_boundaries[i + 1], px[i], fx[i]
            ))
        f.write('\n')


def task_a():
    with open('input.txt', 'r') as f:
        mean_interarrival_time = float(f.readline())
        mean_service_time = float(f.readline())
        total_customers = int(f.readline())

    simulator = Simulator(mean_interarrival_time, mean_service_time, total_customers)
    simulator.run()

    outputs = simulator.get_statistics()
    with open('output_a.txt', 'w') as f:
        f.write('Average delay in queue: {:.3f}\n'.format(outputs['average_delay_in_queue']))
        f.write('Average queue length:   {:.3f}\n'.format(outputs['average_queue_length']))
        f.write('Server utilization:     {:.3f}\n'.format(outputs['server_utilization']))
        f.write('Time simulation ended:  {:.3f}\n'.format(outputs['time_simulation_ended']))

    interarrival_rv_pairs, service_rv_pairs = simulator.get_rv_pairs()

    ix = [urv for urv, erv in interarrival_rv_pairs]
    iy = [erv for urv, erv in interarrival_rv_pairs]
    sx = [urv for urv, erv in service_rv_pairs]
    sy = [erv for urv, erv in service_rv_pairs]

    plt.scatter(ix, iy)
    plt.title('Uni vs Expo - interarrival time')
    if PLOT:
        plt.show()
    plt.scatter(sx, sy)
    plt.title('Uni vs Expo - service time')
    if PLOT:
        plt.show()

    write_statistics('Uniform', ix + sx)
    write_statistics('Interarrival', iy, mean_interarrival_time)
    write_statistics('Service', sy, mean_service_time)


def task_b():
    with open('input.txt', 'r') as f:
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

    with open('output_b.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(table)

    data = table[1:]
    for i in range(1, 5):
        plt.plot([x[0] for x in data], [x[i] for x in data])
        plt.title(table[0][i] + ' - vs - k')
        if PLOT:
            plt.show()


def main():
    task_a()
    task_b()


if __name__ == '__main__':
    main()
