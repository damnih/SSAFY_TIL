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
    map_data.extend([[ '' for c in range(map_width)] for r in range(map_height)])
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

NICKNAME = '서울2_함다민'
game_data = init(NICKNAME)

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


###################
    # 탱크의 동작을 결정하기 위한 알고리즘을 구현하고 원하는 커맨드를 output 변수에 담기
    # 코드 구현 예시: '아래쪽으로 전진'하되, 아래쪽이 지나갈 수 있는 길이 아니라면 '오른쪽로 전진'하라

    # 일단 그냥 무지성으로 bfs돌릴까?

    # output = 'A'  # 알고리즘에 의해 커맨드를 결정하기 전 임시로 A 지정

    sero = len(map_data)
    garo = len(map_data[0])
    visited = [[-1] * garo for _ in range(sero)]

#     print(f"""제대로 되었는지 확인 세로{sero} 가로{garo}
#         맵 데이터 확인
#         {map_data}
# """)
    # 이거 그냥 렌으로 하는 게 맞음 맵 데이터는 진짜 맵 데이터만 나옴

    for i in range(sero):
        for j in range(garo):
            if map_data[i][j] == 'A':
                my_position = [i, j]
                break

    # stack = []
    #
    # dr = [-1, 1, 0, 0]
    # dc = [0, 0, -1, 1]
    #
    # while stack:
    #     now_node = stack.pop()
    #
    #     now_r = now_node[0]
    #     now_c = now_node[1]
    #
    #     visited[now_r][now_c] = 1
    #     for dir in range(4):
    #         new_r = now_r + dr[dir]
    #         new_c = now_c + dc[dir]
    #
    #         if 0 <= new_r < sero and 0 <= new_c < garo:
    #             if map_data[new_r][new_c] == 'F':
    #                 print(dir)
    #             if map_data[new_r][new_c] == 'G':
    #                 if visited[new_r][new_c] == -1:
    #                     next_node = [new_r, new_c]
    #                     stack.append(next_node)




    dr = [1, 0, 0, -1] # 하, ......, 상
    dc = [0, -1, 1, 0] # .., 좌, 우, ..

    command_dir = ['D ', 'L ', 'R ', 'U ']

    true_command = []
    start = my_position + ['U A']
    

# 나의 오류:
# 한 스테이지에 두 판이 도는데 
# 첫 판을 끝내면 다음 판이 진행되지 않고 이전 인풋이 계속 이어졌음 
# 그니깐 한마디로 지금 찾는 위치가 들어가있지 않았다는 거임 

# 왜?? by 이승원
# # # visited가 초기화가 되지 않아서 문제가 생겼다 
# 코드는 한번만 실행함 
# 즉 한 번 실행한 코드가 while문 안에서 계속 돌고 돌고 돌고 하는 것이었기 때문에
# 한 스테이지가 끝날 때마다 그 동작 자체가 계속 새롭게 시작되었어야 하는 거임 

# 걍.. 외부에 dfs bfs 코드를 함수로 정의해두고, 
# 그걸 끌어다 썼으면 문제가 안 생겼을지도,,, 

    visited = [[-1] * garo for _ in range(sero)] # 요놈이초기화되지않는게문제!!!!!! 

    stack = [start]
    while stack:
        now_node = stack.pop()
        now_r = now_node[0]
        now_c = now_node[1]
        print(f'now_node {now_node}')
        visited[now_r][now_c] = 2
        output = now_node[2]
        game_data = submit(output)

        for dir in range(4):
            next_r = now_r + dr[dir]
            next_c = now_c + dc[dir]

            if 0 <= next_r < sero and 0 <= next_c < garo:
                print(f"next_r, next_c = {next_r},{next_c}")
                # 방문 안한 곳이라면
                if visited[next_r][next_c] == -1:
                    # 목표점이라면
                    print(f'다음 노드의 정보:{map_data[next_r][next_c]}')

                    if map_data[next_r][next_c] == 'X':
                        next_node = [now_r, now_c, command_dir[dir] + 'F']
                        # true_command.append(command_dir[dir] + 'F')
                        # break
                        stack = []
                        stack.append(next_node)
                    # 풀지대라면
                    if map_data[next_r][next_c] == 'G':
                        # 그제서야 그머냐 다음노드로 스택에 넣어줘
                        next_node = [next_r, next_c, command_dir[dir] + 'A']
                        true_command.append(command_dir[dir] + 'A')
                        print(f"next_node {next_node}")
                        stack.append(next_node)

    # for cmd in true_command:
    #     output = cmd
    #     game_data = submit(output)



'''
    dr = [1, 0, 0, -1] # 하, ......, 상
    dc = [0, -1, 1, 0] # .., 좌, 우, ..

    command_dir = ['D ', 'L ', 'R ', 'U ']

    true_command = []
    start = my_position + ['U A']

    visited = [[-1] * garo for _ in range(sero)]

    stack = [start]
    while stack:
        now_node = stack.pop()
        now_r = now_node[0]
        now_c = now_node[1]
        print(f'now_node {now_node}')
        visited[now_r][now_c] = 2
        # output = now_node[2]
        # game_data = submit(output)

        for dir in range(4):
            next_r = now_r + dr[dir]
            next_c = now_c + dc[dir]

            if 0 <= next_r < sero and 0 <= next_c < garo:
                print(f"next_r, next_c = {next_r},{next_c}")
                # 방문 안한 곳이라면
                if visited[next_r][next_c] == -1:
                    # 목표점이라면
                    print(f'다음 노드의 정보:{map_data[next_r][next_c]}')

                    if map_data[next_r][next_c] == 'X':
                        next_node = [now_r, now_c, command_dir[dir] + 'F']
                        true_command.append(command_dir[dir] + 'F')
                        true_command.append(command_dir[dir] + 'F')
                        true_command.append(command_dir[dir] + 'F')
                        true_command.append(command_dir[dir] + 'F')
                        break
                        # stack.append(next_node)
                    # 풀지대라면
                    if map_data[next_r][next_c] == 'G':
                        # 그제서야 그머냐 다음노드로 스택에 넣어줘
                        next_node = [next_r, next_c, command_dir[dir] + 'A']
                        true_command.append(command_dir[dir] + 'A')
                        print(f"next_node {next_node}")
                        stack.append(next_node)

    for cmd in true_command:
        output = cmd
        game_data = submit(output)

'''






# 그냥 진짜 무지성으로 길만 찾아보자
# dfs 돌리는거임

'''
stack = []

dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

while stack:
    now_node = stack.pop()
    
    
    now_r = now_node[0]
    now_c = now_node[1]
    
    visited[now_r][now_c] = 1 
    for dir in range(4): 
        new_r = now_r + dr[dir]
        new_c = now_c + dc[dir]
        
        if 0 <= new_r < sero and 0 <= new_c < garo:
            if visited[new_r][new_c] == -1:
                next_node = [new_r, new_c]
                stack.append(next_node)

'''





'''

    visited[start[0]][start[1]] = 7

    dr = [-1, 1, 0, 0] # 상, 하, ......
    dc = [0, 0, -1, 1] # ......, 좌, 우

    command_dir = ['U ', 'D ', 'L ', 'R ']

    stack = [start]

    while stack:
        now_node = stack.pop()
        visited[now_node[0]][now_node[1]] = 6
        print(now_node)
        # print(visited)

        output = now_node[2]
        game_data = submit(output)


        for dir in range(4):
            next_r = now_node[0] + dr[dir]
            next_c = now_node[1] + dc[dir]

            if 0 <= next_r < sero and 0 <= next_c < garo:
                print(f"next_r, next_c = {next_r},{next_c}")
                if visited[next_r][next_c] == -1:
                    if map_data[next_r][next_c] == 'G':
                        next_node = [next_r, next_c, command_dir[dir] + 'A']
                        stack.append(next_node)


'''



'''


    while queue:

        now_node = queue.pop(0)
        output = now_node[2]

        print(output)
        print(visited[now_node[0]][now_node[1]])

        game_data = submit(output)
        # for dir in range(4):
        #     for fire_range in range(1, 3):
        #         next_r = now_node[0] + dr[dir] * fire_range
        #         next_c = now_node[1] + dc[dir] * fire_range
        #         if 0 <= next_r < garo and 0 <= next_c < sero: # 여기까지는 벽 처리
        #             if map_data[next_r][next_c] == 'X': # 만약 사정거리 내에 적의 포탑이 있다면
        #                 output = command_dir[dir] + " F"
        #                 # print(output)
        #                 break
        #     break

        for dir in range(4):
            next_r = now_node[0] + dr[dir]
            next_c = now_node[1] + dc[dir]
            if 0 <= next_r < sero and 0 <= next_c < garo:  # 여기까지는 벽 처리
                # 만약 그 길이 풀이고 방문한 적 없다면
                if map_data[next_r][next_c] == 'G' and visited[next_r][next_c] == -1:
                    # 방문처리 해주고
                    visited[next_r][next_c] = visited[now_node[0]][now_node[1]] + 1

                    next_node = [next_r, next_c, command_dir[dir] + 'A']
                    queue.append(next_node)
                    print(queue)
                if map_data[next_r][next_c] == 'X':
                    next_node = [next_r, next_c, command_dir[dir] + 'F']


# 아니 이거 지금 문제인게 뭐냐면?? 지금 이게 방문처리가 안되고있음 잠시만 확인을 해봐야겠어
# 아니 미친 방문처리 되었는데도 걍 가고 있는데?? 이게 머임??


        # if map_data[next_r][next_c] == 'G':
        # 얘가 일단 풀이라면 지나갈 수 있어
        # 걍 내 로직은 단순하게 가자. 걍 풀인 곳을 계속 탐색하면서 적의 포탑인 X가 나올 떄까지 ㄱㄱ 하는거
        # 근데 내가 움직이기 전에, 만약에 사정거리(1~3) 내에 적의 포탑이 있다면?
        # 그 방향으로 포탄 쏘기 ㄱㄱㄱ
        # 일반 미사일 F 메가미사일 M임



'''

    # # my_position = [-1, -1]
    # # for i in range(len(map_data)):
    # #     for j in range(len(map_data[0])):
    # #         if map_data[i][j] == 'A':
    # #             my_position[0] = i
    # #             my_position[1] = j
    # #             break
    # #     if my_position[0] > 0: break
    #
    # if my_position[0] < len(map_data) - 1 and map_data[my_position[0] + 1][my_position[1]] == 'G':
    #     output = 'D A'
    # else:
    #     output = 'R A'

    # 일단 여기서 먼저 준 코드는 딱 전진(아래방향, 오른쪽방향)만 하는 코드

    # 그렇다면 내가 생각해야 할 거는 머다?
    # 얘가 어느 상황에서 어떤 조건에 따라 방향이 틀려지고 어떤 커맨드를 받을 것인지 그게 중요하다
    #
    #
    # 일단 갈 수 있는 경우의 수
    # 1) 풀





    # while 문의 끝에는 다음 코드가 필수로 존재하여야 함
    # output에 담긴 값은 submit 함수를 통해 배틀싸피 메인 프로그램에 전달
    # game_data = submit(output)


# 반복문을 빠져나왔을 때 배틀싸피 메인 프로그램과의 연결을 완전히 해제하기 위해 close 함수 호출
close()