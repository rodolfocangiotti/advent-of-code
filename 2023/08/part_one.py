import os


def my_directory():
    return os.path.dirname(__file__)


def read_file(file):
    file = os.path.join(my_directory(), file)
    with open(file, mode='r') as f:
        txt = f.read()
    return txt.strip()


def get_step_pattern(data):
    first_line, *_ = data.split('\n')
    return tuple(first_line.strip())


def get_node_map(data):
    _, _, *nodes = data.split('\n')
    result = {}
    for node in nodes:
        starting_node, destinations = node.split(' = ')
        destination_nodes = destinations[1:-1].split(', ')
        result[starting_node] = destination_nodes
    return result


def optimize_node_map(node_map, step_pattern):
    result = {}
    for start, destinations in node_map.items():
        for step in step_pattern:
            if step == 'L':
                next_node = destinations[0]
            elif step == 'R':
                next_node = destinations[1]
            else:
                raise ValueError
            destinations = node_map[next_node]
        result[start] = next_node
    return result


def find_path_steps(node_map, step_pattern):
    current = 'AAA'
    steps = 0
    while current != 'ZZZ':
        current = node_map[current]
        steps += 1
    return steps * len(step_pattern)


def main():
    data = read_file('input_data.txt')
    step_pattern = get_step_pattern(data)
    node_map = get_node_map(data)
    node_map = optimize_node_map(node_map, step_pattern)
    steps = find_path_steps(node_map, step_pattern)

    print(f'Result: {steps}')


if __name__ == '__main__':
    main()
