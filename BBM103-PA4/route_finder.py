def cost_field(input_file):
    with open(input_file ,'r') as file:
        lines = file.readlines()
        costs = []
        for item in lines[0].strip().split():
            costs.append((item))
        cost1 = int(costs[0])
        cost2 = int(costs[1])
        cost3 = int(costs[2])
        field = [[int(value) for value in line.strip().split()] for line in lines[1:]]
        return cost1, cost2, cost3, field

def move(x, y, field):
    try:
        return field[x][y]
    except IndexError:
        return False
def is_valid_move(field, visited, x, y):
    return move(x, y, field) == 1 and not visited[x][y]

def calculate_cost(x, y, field, cost1, cost2, cost3):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # horizontal and vertical neighborhoods
    diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # diagonal neighborhoods

    horizontal_vertical_sinkhole_count = 0
    diagonals_sinkhole_count = 0

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(field) and 0 <= ny < len(field[0]) and field[nx][ny] == 0:
            horizontal_vertical_sinkhole_count += 1

    for dx, dy in diagonals:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(field) and 0 <= ny < len(field[0]) and field[nx][ny] == 0:
            diagonals_sinkhole_count += 1

    if horizontal_vertical_sinkhole_count == 0 and diagonals_sinkhole_count == 0:
        return cost1
    elif diagonals_sinkhole_count == 0 and horizontal_vertical_sinkhole_count >= 0:
        return cost3
    elif horizontal_vertical_sinkhole_count > 0:
        return cost3
    else:
        return cost2

def find_cheapest_path(field, cost1, cost2, cost3, visited, memo, x, y, path, current_cost, min_cost):
    rows, columns = len(field), len(field[0])

    if y == columns - 1:
        current_cost += calculate_cost(x, y, field, cost1, cost2, cost3)
        if current_cost < min_cost[0]:
            min_cost[0] = current_cost
            min_cost[1] = [path[:]]
        elif current_cost == min_cost[0]:
            min_cost[1].append(path[:])
        return

    if (x, y) in memo and memo[(x, y)] <= current_cost:
        return

    directions = [(0, 1), (-1, 0), (1, 0), (0, -1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < columns and not visited[nx][ny] and field[nx][ny] == 1:
            move_cost = calculate_cost(nx, ny, field, cost1, cost2, cost3)
            visited[nx][ny] = True
            path.append((nx, ny))
            find_cheapest_path(field, cost1, cost2, cost3, visited, memo, nx, ny, path, current_cost + move_cost, min_cost)
            path.pop()
            visited[nx][ny] = False

    memo[(x, y)] = current_cost

def mark_path(field, path):
    for x, y in path:
        field[x][y] = 'X'
    return field

def write_output(output_file, field, min_cost):
    with open(output_file, 'w') as file:
        if min_cost[0] == float('inf'):
            file.write('There is no possible route!')
        else:
            file.write(f'Cost of the route: {min_cost[0]-1}\n')
            field = mark_path(field, min_cost[1][0])
            for i, row in enumerate(field):
                file.write(" ".join(str(value) if value != 'X' else 'X' for value in row))
                if i < len(field) - 1:
                    file.write("\n")

def main():
    input_file = 'input.txt'
    output_file = 'output.txt'
    cost1, cost2, cost3, field = cost_field(input_file)

    rows, columns = len(field), len(field[0])
    visited = [[False for _ in range(columns)] for _ in range(rows)]
    memo = {}
    min_cost = [float('inf'), []]

    for i in range(rows):
        if field[i][0] == 1:
            visited[i][0] = True
            move_cost = calculate_cost(i, 0, field, cost1, cost2, cost3)
            find_cheapest_path(field, cost1, cost2, cost3, visited, memo, i, 0, [(i, 0)], move_cost, min_cost)
            visited[i][0] = False

    write_output(output_file, field, min_cost)

if __name__ == '__main__':
    main()