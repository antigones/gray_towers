from gray_hanoi import GrayHanoi
from gray_bucharest import GrayBucharest


def main():

    gray_hanoi = GrayHanoi(n_rigs=3, n_disks=3)
    configurations = gray_hanoi.solve()

    for configuration in configurations:
        print(configuration)

    gray_bucharest = GrayBucharest(n_rigs=3, n_disks=3)
    configurations = gray_bucharest.solve()

    ternary_gray_sequence = [[0, 0, 0], [0, 0, 1], [0, 0, 2],
                             [0, 1, 2], [0, 1, 1], [0, 1, 0],
                             [0, 2, 0], [0, 2, 1], [0, 2, 2],
                             [1, 2, 2], [1, 2, 1], [1, 2, 0],
                             [1, 1, 0], [1, 1, 1], [1, 1, 2],
                             [1, 0, 2], [1, 0, 1], [1, 0, 0],
                             [2, 0, 0], [2, 0, 1], [2, 0, 2],
                             [2, 1, 2], [2, 1, 1], [2, 1, 0],
                             [2, 2, 0], [2, 2, 1], [2, 2, 2]]
    for i, configuration in enumerate(configurations):
        print('towers={0}, gray={1}'.format(
            configuration, ternary_gray_sequence[i]))


if __name__ == "__main__":
    main()
