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


NICKNAME = '서울2_조영우'
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

    # 탱크의 동작을 결정하기 위한 알고리즘을 구현하고 원하는 커맨드를 output 변수에 담기

    di_dj_key = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
    di_dj = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    ENEMY = ['E1', 'E2', 'E3']
    obstacles = ['T', 'R']
    # print(enemies)
    normal_round = int(allies['A'][2])
    mega_round = int(allies['A'][3])

    print(f'normal_round : {normal_round}')
    print(f'mega_round : {mega_round}')


    def can_shoot(cur_i, cur_j):
        """
        현재 위치를 기반으로 내 탱크 사거리 안에
            1. 터렛이 있으면 터트린다
                그 전에 터렛과 나 사이에 장애물이 있는지 확인한다

        """
        global output
        # 사거리 내 순회
        for multi in range(1, FIRE_RANGE + 1):
            # 방향벡터와 커맨드 이름을 같이 전달, 유효할 때 바로 커맨드 입력
            for di, dj, com_key in di_dj_key:
                tar_i = cur_i + di * multi
                tar_j = cur_j + dj * multi
                # 사거리 내에서 상하좌우 살펴보다(값이 유효할 때만) 터렛을 발견했다면
                if 0 <= tar_i < len(map_data) and 0 <= tar_j < len(map_data):
                    if map_data[tar_i][tar_j] == 'X' and normal_round:
                        # 진짜 쏴도 되는지 확인하자
                        is_it_real = True
                        # 사거리 2나 3일때 그 사이를 확인한다
                        # 1일때는 쏴도 된다
                        if multi != 1:
                            for multi_b in range(1, multi):
                                tar_i_b = cur_i + di * multi_b
                                tar_j_b = cur_j + dj * multi_b
                                # 나무나 돌이 사이에 있음을 발견하면 쏘지말라고 False
                                if map_data[tar_i_b][tar_j_b] in obstacles:
                                    is_it_real = False
                        # 장애물이 없음이 확인되면 쏴버리기 (탄 있으면)
                        if is_it_real and normal_round:
                            output = com_key + ' F'
                            return True
                    # 터렛이 아니라 적 탱크를 발견했다면
                    elif map_data[tar_i][tar_j] in ENEMY and mega_round:
                        is_it_real = True
                        # 사거리 2나 3일때 그 사이를 확인한다
                        # 1일때는 쏴도 된다
                        if multi != 1:
                            for multi_b in range(1, multi):
                                tar_i_b = cur_i + di * multi_b
                                tar_j_b = cur_j + dj * multi_b
                                # 나무나 돌이 사이에 있음을 발견하면 쏘지말라고 False
                                if map_data[tar_i_b][tar_j_b] in obstacles:
                                    is_it_real = False
                        # 장애물이 없음이 확인되면 쏴버리기 (탄 있으면)
                        if is_it_real and mega_round:
                            output = com_key + ' F M'
                            return True

        # 여기까지 함수가 진행됬으면 못쏘는겁니다
        return False


    def bfs(input_cur_i, input_cur_j, num1_round, num2_round):
        """
        주어진 좌표와 탄 수를 기반으로
        주어진 위치에서 터렛까지의 최단거리를 구하는 함수
        """
        goal_i = turret_position[0]
        goal_j = turret_position[1]
        len_map_data = len(map_data)
        # 방문배열 초기화
        visited = [[0] * len_map_data for _ in range(len_map_data)]
        # 함수가 실행된 위치가 나무라면 이미 메가탄을 한번 쐈다는 가정하에 진행
        if map_data[input_cur_i][input_cur_j] == 'T':
            num2_round -= 1

        # 입력좌표 i, 입력좌표 j, 진행 거리(bfs), 일반탄 수, 메가탄 수
        q = [(input_cur_i, input_cur_j, 0, num1_round, num2_round)]
        # 시작 위치 방문처리
        visited[input_cur_i][input_cur_j] = 1

        # bfs 시작
        while q:
            cur_i, cur_j, cur_distance, num1, num2 = q.pop(0)

            # if map_data[cur_i][cur_j] in ENEMY:
            #     return cur_distance
            
            if cur_i == goal_i and cur_j == goal_j:
                return cur_distance

            for di, dj in di_dj:
                new_i = cur_i + di
                new_j = cur_j + dj
                # 인덱스 에러 방지 유효한 값일때
                if 0 <= new_i < len_map_data and 0 <= new_j < len_map_data:
                    # 터렛 발견시 종료, 최단거리 반환
                    if map_data[new_i][new_j] == 'X':
                        return cur_distance + 1

                    # 갈수 있는 지형이고 방문하지 않았다면 추가
                    if map_data[new_i][new_j] == 'G' and not visited[new_i][new_j]:
                        q.append((new_i, new_j, cur_distance + 1, num1, num2))
                        visited[new_i][new_j] = 1

                    # 다음 후보지가 나무이지만 부술 메가탄이 있고 방문하지 않았다면 큐에 추가
                    if map_data[new_i][new_j] == 'T' and (num1 or num2) and not visited[new_i][new_j]:
                        q.append((new_i, new_j, cur_distance + 1, num1 - 1, num2))
                        visited[new_i][new_j] = 1

                    # 다음 후보지가 탱크이지만 부술 메가탄이 있고 방문하지 않았다면 큐에 추가
                    if map_data[new_i][new_j] in ENEMY and (num2 or num1) and not visited[new_i][new_j]:
                        q.append((new_i, new_j, cur_distance + 1, num1 - 1, num2))
                        visited[new_i][new_j] = 1

        return -1


    def choose_next(cur_i, cur_j):
        """
        현재 위치 기반 데이터를 종합해 어떤 커맨드를 줄지 정하는 함수
        """
        global normal_round, mega_round
        next_lst = []  # 갈 수 있는 후보지 리스트
        next_go = str()  # 커맨드 초기값
        min_v = float('inf')  # 최소값 초기값
        next_stop_i = 0  # 이동한다면 행값
        next_stop_j = 0  # 이동한다면 열값

        for di, dj, com_key in di_dj_key:
            next_i = cur_i + di
            next_j = cur_j + dj
            # 유효한 값이며
            if 0 <= next_i < len(map_data) and 0 <= next_j < len(map_data):
                # 지나갈수 있거나, (탄이 있는 상태에서 나무이거나) 의 위치들을 후보지에 등록
                if map_data[next_i][next_j] == 'G' or (map_data[next_i][next_j] == 'T' and (normal_round or mega_round)):
                    next_lst.append((next_i, next_j, com_key))

        # 후보지들 순환, 이 중에서 bfs 돌려서 제일 목적지까지 거리가 짧은 위치로 이동할것임
        print(f'nextlst is {next_lst}##############')
        for next_opt in next_lst:
            next_i_a, next_j_b, com_key_c = next_opt
            # bfs 실행
            cur_value = bfs(next_i_a, next_j_b, normal_round, mega_round)
            # bfs 실행 후 값이 유효하고 최소값 갱신가능하다면 갱신
            if cur_value != -1 and cur_value < min_v:
                min_v = cur_value  # 최소값 갱신
                next_go = com_key_c  # 커맨드 키 저장
                next_stop_i = next_i_a  # 행값 저장
                next_stop_j = next_j_b  # 열값 저장

        print(f'nextgo is {next_go} #############')
        # 유효하다면
        if next_go:
            print(next_go)
            # 최종 결정지가 나무로 진행해야하는 것이라면 나무를 부수는 커맨드 입력
            if map_data[next_stop_i][next_stop_j] == 'T':
                if normal_round >= 0:
                    return next_go + ' F'
                elif mega_round >= 0:
                    return next_go + ' F M'
            # 나무가 아니라면 이동 커맨드 입력
            return next_go + ' A'

        # 유효하지 않으면 모르겠다..일단이동
        else:
            print('something went wrong!!!!!!!!!!!!!!!!')
            return 'A'

    output = 'A'  # 알고리즘에 의해 커맨드를 결정하기 전 임시로 A 지정

    FIRE_RANGE = 3

    # 내 위치 찾는 부분
    my_position = [-1, -1]
    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            if map_data[i][j] == 'A':
                my_position[0] = i
                my_position[1] = j
                break
        if my_position[0] > 0:
            break

    # 목적지 찾는 부분
    turret_position = [-1, -1]
    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            if map_data[i][j] == 'X':
                turret_position[0] = i
                turret_position[1] = j
                break
        if turret_position[0] > 0:
            break

    if turret_position[0] < len(map_data)//2:
        for i in range(turret_position[0], turret_position[0]+3):
            for j in range(turret_position[1]-2, turret_position[1]+1):
                map_data[i][j] = 'Z'
    else:
        for i in range(turret_position[0]-2, turret_position[0]+1):
            for j in range(turret_position[1], turret_position[1]+3):
                map_data[i][j] = 'Z'

    # 당장 쏠 수 있다면 쏘지만 그게 아니라면 다음 위치를 정한다
    if not can_shoot(my_position[0], my_position[1]):
        """
        여기서 갈 수 있는 상하좌우 위치 기준으로 bfs 를 돌리고
        각각의 값 중 최소값 위치를 구해서 어디로 가는게 맞는 판단인지를 구하자
        """
        print("let's go")
        output = choose_next(my_position[0], my_position[1])

    # while 문의 끝에는 다음 코드가 필수로 존재하여야 함
    # output에 담긴 값은 submit 함수를 통해 배틀싸    print(output)피 메인 프로그램에 전달
    print(enemies)
    print(output)

    game_data = submit(output)


# 반복문을 빠져나왔을 때 배틀싸피 메인 프로그램과의 연결을 완전히 해제하기 위해 close 함수 호출
close()
