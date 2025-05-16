# 가장 많은 팀이 체육관을 사용
#
# 이거 그거다 신범수가 소트 두 번 써야 한다고 했던 그거다

'''
3
8 16
6
11 14
15 17
10 12
7 9
10 11
15 16
8 18
6
3 4
3 5
17 20
12 14
13 16
16 17
10 16
6
8 9
12 14
15 16
12 15
10 12
5 6

1 20
7
6 7
6 14
8 12
9 13
9 10
7 9
7 15


'''

def how_many_teams(open, close, register_list):
    pivot = open # 일단 기준점은 오픈시간임 오픈시간 이후부터 연습할 애들 찾아줄거니깐
    used_team = 0 # 아직 사용한 애들은 없고
    i = 0
    while i < N :
        if register_list[i][0] >= pivot: # 만약 사용시작시간이 기준점보다 늦다면 그제서야 사용 가능
            endtime = register_list[i][1] # 이 녀석의 끝나는 시간을 찾아
            if endtime > close: # 만약 이 끝나는 시간이 체육관 사용시간보다 늦다면 사용 불가능하니깐 그냥 그대로 break
                break
            pivot = endtime # 위의 이프문에 안걸린,, 사용시간 내라면, 기준점은 다시 이 끝나는 시간으로 설정
            used_team += 1 # 사용할 수 있었으니깐 사용팀 개수 늘려주깅
            # print(used_team)
        # 위의 이프문(기준점보다 시작점이 늦은 경우)에 안 걸렸다면
        # (=즉 기준점보다 빨리 시작해서 사용이 불가능한 경우라면) 인덱스 증가시켜가면서 찾아내기
        i += 1
    # 반복문 다 끝나면 총 사용 팀 수가 나옴 이걸 반환
    return used_team



T = int(input())

for tc in range(1, T + 1):
    open, close = map(int, input().split())
    N = int(input()) # 신청 팀 수
    register_list = []
    for i in range(N):
        team_time = list(map(int, input().split()))
        register_list.append(team_time)

    # print(register_list)

    # 체육관을 여는 시간 이전이나 닫는 시간 이후를 이용 시간에 포함시킨 팀은 제외제외제외

    # 일단 레지스터 리스트를 소트해야됨
    register_list.sort(key = lambda x : x[1])
    # print(register_list)

    register_list.sort(key = lambda x : x[0])
    # print(register_list)
    # 오키 내가 원하는 대로 정렬 완료


    # open, close = 8, 16
    # N = 6
    # register_list = [[7, 9], [10, 11], [10, 12], [11, 14], [15, 16], [15, 17]]


    ans = how_many_teams(open, close, register_list)
    print(f"#{tc} {ans}")





# print(used_team)
#
# #
# use_end = 0
# used_team = 0
# canuse = open
# while use_end <= close:
#     # 일단 맨 처음 원소가 기준점보다 늦게 신청했는지 확인
#     for i in range(N):
#         if register_list[i][0] >= canuse:
#             use_start = i
#             break
#     use_end = register_list[use_start][1]
#     # 그렇다면 이 use_end 이후로 위의 과정 반복
#     canuse = use_end
#     used_team += 1 # 그머냐 사용한 팀 수 증가
#     if canuse == close:
#         break
#
# print(used_team)
#

