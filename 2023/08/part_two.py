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


def _find_nodes_ending_with(node_map, pattern):
    return tuple(node for node in node_map.keys() if node.endswith(pattern))


def find_start_nodes(node_map):
    return _find_nodes_ending_with(node_map, 'A')


def find_end_nodes(node_map):
    return _find_nodes_ending_with(node_map, 'Z')


# def find_path_steps(node_map, step_pattern):
#     start_nodes = find_start_nodes(node_map)
#     end_nodes = find_end_nodes(node_map)
#     current = start_nodes
#     steps = 0
#     while current != end_nodes:
#         current = tuple(node_map[node] for node in current)
#         steps += 1
#     return steps * len(step_pattern)


def find_path_steps(start, target, node_map, step_pattern):
    history = {start}
    current = start
    steps = 0
    while current != target:
        current = node_map[current]
        if current in history:
            raise Exception('Loop detected.')
        history.add(current)
        steps += 1
    return steps * len(step_pattern)


def prime_factors(n):
    result = {}
    while n > 1:
        for d in range(2, n + 1):
            if n % d == 0:
                n //= d
                result[d] = result.get(d, 0) + 1
                break
    return result


def get_lcm(iterable):
    maximums = {}
    for n in iterable:
        factors = prime_factors(n)
        for m, p in factors.items():
            maximums[m] = max(p, maximums.get(m, 0))

    result = 1
    for n, m in maximums.items():
        result *= n ** m
    return result


def main():
    data = read_file('input_data.txt')
    step_pattern = get_step_pattern(data)
    node_map = get_node_map(data)
    node_map = optimize_node_map(node_map, step_pattern)

    start_nodes = find_start_nodes(node_map)
    end_nodes = find_end_nodes(node_map)
    steps_found = []
    m = len(start_nodes)
    for n, start_node in enumerate(start_nodes, 1):
        for end_node in end_nodes:
            try:
                steps_found.append(find_path_steps(start_node, end_node, node_map, step_pattern))
                break
            except Exception:
                continue
        else:
            raise Exception('Path not found.')
        print(f'Path {n} / {m} done.')

    steps = get_lcm(steps_found)
    print(f'Result: {steps}')


if __name__ == '__main__':
    main()
