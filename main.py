from gray_hanoi import GrayHanoi
from gray_bucharest import GrayBucharest
from hanoi_tower_qlearning import HanoiTowerQLearning


def main():

    gray_hanoi = GrayHanoi(n_pegs=3, n_disks=3)
    configurations = gray_hanoi.solve(verbose=True)

    for configuration in configurations:
        print(configuration)

    gray_bucharest = GrayBucharest(n_pegs=3, n_disks=3)
    configurations = gray_bucharest.solve()

    """"
    ternary_gray_sequence = [
        [0, 0, 0], [0, 0, 1], [0, 0, 2],
        [0, 1, 2], [0, 1, 1], [0, 1, 0],
        [0, 2, 0], [0, 2, 1], [0, 2, 2],
        [1, 2, 2], [1, 2, 1], [1, 2, 0],
        [1, 1, 0], [1, 1, 1], [1, 1, 2],
        [1, 0, 2], [1, 0, 1], [1, 0, 0],
        [2, 0, 0], [2, 0, 1], [2, 0, 2],
        [2, 1, 2], [2, 1, 1], [2, 1, 0],
        [2, 2, 0], [2, 2, 1], [2, 2, 2]
    ]
    """
    ternary_gray_sequence = gray_hanoi.generate_m_ary_gray_code(3)
    for configuration, tgs in zip(configurations, ternary_gray_sequence):
        print(f'towers={configuration}, gray={tgs}')




if __name__ == "__main__":
    main()
