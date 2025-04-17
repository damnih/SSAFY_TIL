import socket

HOST = '127.0.0.1'
PORT = 8747

# 입력 데이터 분류
char_to_int = {'U': 0, 'R': 1, 'D': 2, 'L': 3}
map_data = [[]]  # 맵 정보. 예) map_data[0][1] - [0, 1]의 지형/지물
allies = {}  # 아군 정보. 예) allies['A'] - 플레이어 본인의 정보
enemies = {}  # 적군 정보. 예) enemies['X'] - 적 포탑의 정보
codes = []  # 주어진 암호문. 예) codes[0] - 첫 번째 암호문

sock = socket.socket()


def init(nickname) -> str:
    try:
        print(f'[STATUS] Trying to connect to {HOST}:{PORT}')
        sock.connect((HOST, PORT))
        print('[STATUS] Connected')
        init_command = f'INIT {nickname}'

        return submit(init_command)

    except Exception as e:
        print('[ERROR] Failed to connect. Please check if Battle SSAFY is waiting for connection.')
        print(e)


def submit(string_to_send) -> str:
    try:
        sock.send((string_to_send + ' ').encode('utf-8'))

        return receive()

    except Exception as e:
        print('[ERROR] Failed to connect. Please check if Battle SSAFY is waiting for connection.')

    return None


def receive() -> str:
    try:
        game_data = (sock.recv(1024)).decode()

        if int(game_data[0]) > 0:
            return game_data

        close()
    except Exception as e:
        print('[ERROR] Failed to connect. Please check if Battle SSAFY is waiting for connection.')


def close():
    try:
        if sock is not None: sock.close()
        print('[STATUS] Connection closed')

    except Exception as e:
        print('[ERROR] Network connection has been corrupted.')


# 입력 데이터를 파싱하여 변수에 저장
def parse_data(game_data):
    # 입력 데이터를 행으로 나누기
    game_data_rows = game_data.split('\n')
    row_index = 0

    # 첫 번째 행 데이터 읽기
    header = game_data_rows[row_index].split(' ')
    map_height = int(header[0])  # 맵의 세로 크기
    map_width = int(header[1])  # 맵의 가로 크기
    num_of_allies = int(header[2])  # 아군의 수
    num_of_enemies = int(header[3])  # 적군의 수
    num_of_codes = int(header[4])  # 암호문의 수
    row_index += 1

    # 기존의 맵 정보를 초기화하고 다시 읽어오기
    map_data.clear()
    map_data.extend([['' for c in range(map_width)] for r in range(map_height)])
    for i in range(0, map_height):
        col = game_data_rows[row_index + i].split(' ')
        for j in range(0, map_width):
            map_data[i][j] = col[j]
    row_index += map_height

    # 기존의 아군 정보를 초기화하고 다시 읽어오기
    allies.clear()
    for i in range(row_index, row_index + num_of_allies):
        ally = game_data_rows[i].split(' ')
        ally_name = ally.pop(0)
        allies[ally_name] = ally
    row_index += num_of_allies

    # 기존의 적군 정보를 초기화하고 다시 읽어오기
    enemies.clear()
    for i in range(row_index, row_index + num_of_enemies):
        enemy = game_data_rows[i].split(' ')
        enemy_name = enemy.pop(0)
        enemies[enemy_name] = enemy
    row_index += num_of_enemies

    # 기존의 암호문 정보를 초기화하고 다시 읽어오기
    codes.clear()
    for i in range(row_index, row_index + num_of_codes):
        codes.append(game_data_rows[i])


NICKNAME = '서울02_이승원'
game_data = init(NICKNAME)

def my_func(game_data):
    try:
        from collections import deque

        def caesar_decode(s, shift=9):
            result = ''
            for c in s:
                if 'A' <= c <= 'Z':
                    result += chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
                else:
                    result += c
            return result

        dr = [0, -1, 0, 1]
        dc = [1, 0, -1, 0]
        parse_data(game_data)
        my_matrix = map_data

        start_position = [-1, -1]
        target_position = [-2, -2]
        target_tank = [-3, -3]

        for i in range(len(map_data)):
            for j in range(len(map_data[0])):
                if map_data[i][j] == 'A':
                    start_position = [i, j]
                if map_data[i][j] == 'X':
                    target_position = [i, j]
                if map_data[i][j] == 'E1':
                    target_tank = [i, j]

        normal_shells = int(allies['A'][2])
        init_mega_shells = int(allies['A'][3])

        H, W = len(map_data), len(map_data[0])
        MAX_MEGA = 10
        visited = [[[[float('inf')] * (MAX_MEGA + 1) for _ in range(2)] for _ in range(W)] for _ in range(H)]
        pq = deque()
        pq.append((start_position[0], start_position[1], None, 0, init_mega_shells, 0))
        visited[start_position[0]][start_position[1]][0][init_mega_shells] = 0
        parent = {}
        parent[(start_position[0], start_position[1], 0, init_mega_shells)] = None
        order = []
        found = False

        # print('[DEBUG] 현재 위치:', row, col)
        # print('[DEBUG] 주변 칸:', [ (row+dr[d], col+dc[d]) for d in range(4) ])
        # print('[DEBUG] 주변 지형:', [ my_matrix[row+dr[d]][col+dc[d]] if 0 <= row+dr[d] < H and 0 <= col+dc[d] < W else '#' for d in range(4) ])
        def is_adjacent_to_f(r, c):
            for d in range(4):
                nr, nc = r + dr[d], c + dc[d]
                if 0 <= nr < H and 0 <= nc < W and my_matrix[nr][nc] == 'F':
                    return True
            return False

        while pq:
            row, col, direct, used_shell, mega_shells, cost = pq.popleft()

            if is_adjacent_to_f(row, col) and codes:
                encrypted = codes[0]
                decoded = caesar_decode(encrypted)
                print('[ENCRYPTED]', encrypted)
                print('[DECODED]', decoded)
                print('[SUBMITTING]', f"G {decoded}")
                return f"G {decoded}"

            if normal_shells > 0 or mega_shells > 0:
                if (target_position[0] + 1 <= row <= target_position[0] + 3 and col == target_position[1]):
                    if row - target_position[0] == 1 or \
                       (row - target_position[0] == 2 and my_matrix[row-1][col] != 'R') or \
                       (row - target_position[0] == 3 and my_matrix[row-1][col] != 'R' and my_matrix[row-2][col] != 'R'):
                        goal_row, goal_col = row, col
                        target_direct = "U M" if mega_shells > 0 else "U F"
                        final_used_shell = used_shell
                        found = True
                        break

                if (target_position[1] - 3 <= col <= target_position[1] - 1 and row == target_position[0]):
                    if target_position[1] - col == 1 or \
                       (target_position[1] - col == 2 and my_matrix[row][col+1] != 'R') or \
                       (target_position[1] - col == 3 and my_matrix[row][col+1] != 'R' and my_matrix[row][col+2] != 'R'):
                        goal_row, goal_col = row, col
                        target_direct = "R M" if mega_shells > 0 else "R F"
                        final_used_shell = used_shell
                        found = True
                        break

            for i in range(4):
                nr = row + dr[i]
                nc = col + dc[i]
                if 0 <= nr < H and 0 <= nc < W:
                    cell = my_matrix[nr][nc]
                    new_mega = min(mega_shells + 1, MAX_MEGA) if cell == 'F' else mega_shells

                    if cell == 'G' or cell == 'F':
                        if cost + 1 < visited[nr][nc][used_shell][new_mega]:
                            visited[nr][nc][used_shell][new_mega] = cost + 1
                            pq.append((nr, nc, i, used_shell, new_mega, cost + 1))
                            parent[(nr, nc, used_shell, new_mega)] = (row, col, used_shell, mega_shells)

                    elif cell in ['T', 'E1'] and used_shell == 0:
                        if cost + 3 < visited[nr][nc][1][new_mega]:
                            visited[nr][nc][1][new_mega] = cost + 3
                            pq.append((nr, nc, i, 1, new_mega, cost + 3))
                            parent[(nr, nc, 1, new_mega)] = (row, col, used_shell, mega_shells)

        if not found:
            return 'S'

        k = (goal_row, goal_col, final_used_shell, mega_shells)
        while k is not None:
            prev = parent.get(k)
            order.append((k[0], k[1]))
            k = prev

        order.reverse()
        order_output = []
        r1, c1 = start_position

        for i in range(len(order) - 1):
            r2, c2 = order[i + 1]
            delta = (r2 - r1, c2 - c1)

            if delta == (1, 0):
                direction = 'D'
            elif delta == (-1, 0):
                direction = 'U'
            elif delta == (0, 1):
                direction = 'R'
            elif delta == (0, -1):
                direction = 'L'
            else:
                r1, c1 = r2, c2
                continue

            if my_matrix[r2][c2] in ['T', 'E1']:
                order_output.append(f'{direction} F')
                order_output.append(f'{direction} A')
                my_matrix[r2][c2] = 'G'
            else:
                order_output.append(f'{direction} A')

            r1, c1 = r2, c2

        r2, c2 = order[0]
        delta = (r2 - start_position[0], c2 - start_position[1])
        if my_matrix[r2][c2] in ['T', 'E1']:
            if delta == (1, 0):
                return 'D'
            elif delta == (-1, 0):
                return 'U'
            elif delta == (0, 1):
                return 'R'
            elif delta == (0, -1):
                return 'L'

        if order_output:
            return order_output[0]
        else:
            return target_direct

    except:
        return 'S'


# while 반복문: 배틀싸피 메인 프로그램과 클라이언트(이 코드)가 데이터를 계속해서 주고받는 부분
while game_data is not None:
    # 자기 차례가 되어 받은 게임정보를 파싱
    print(f'----입력데이터----\n{game_data}\n----------------')
    parse_data(game_data)


    # 파싱한 데이터를 화면에 출력하여 확인
    print(f'\n[맵 정보] ({len(map_data)} x {len(map_data[0])})')
    for i in range(len(map_data)):
        for j in range(len(map_data[i])):
            print(f'{map_data[i][j]} ', end='')
        print()

    print(f'\n[아군 정보] (아군 수: {len(allies)})')
    for k, v in allies.items():
        if k == 'A':
            print(f'A (내 탱크) - 체력: {v[0]}, 방향: {v[1]}, 보유한 일반 포탄: {v[2]}개, 보유한 메가 포탄: {v[3]}개')
        elif k == 'H':
            print(f'H (아군 포탑) - 체력: {v[0]}')
        else:
            print(f'{k} (아군 탱크) - 체력: {v[0]}')

    print(f'\n[적군 정보] (적군 수: {len(enemies)})')
    for k, v in enemies.items():
        if k == 'X':
            print(f'X (적군 포탑) - 체력: {v[0]}')
        else:
            print(f'{k} (적군 탱크) - 체력: {v[0]}')

    print(f'\n[암호문 정보] (암호문 수: {len(codes)})')
    for i in range(len(codes)):
        print(codes[i])
    '''
    턴 마다 bfs 탐색을 통해 목적지까지 최단 거리를 구하고 경로를 추적하여 첫 움직임을 return 해주고 마지막 순간
    목표물과 탱크의 위치를 토대로 발사 방향을 return 해준다.
    상대 탱크가 경로를 막고 서 있으면 bfs 탐색에서 에러가 나는데 그때는 S를 return 해줘서 경로가 열릴때까지 기다린다.
    나무를 부수고 가는 경우가 최대 경로가 될 수 있지만 구현에 실패 했다
    '''
    
    output = my_func(game_data)
    print(output)
    game_data = submit(output)

# 반복문을 빠져나왔을 때 배틀싸피 메인 프로그램과의 연결을 완전히 해제하기 위해 close 함수 호출
close()