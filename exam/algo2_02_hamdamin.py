import heapq

# 전선 길이 구하는 함수 일단 만들어놔야겟다,,

def eleclinelen(start, end):
    a = abs(start[0] - end[0])
    b = abs(start[1] - end[1])
    return a + b

'''
3

4
5 2
8 4
8 2
10 3

3
-5 0
-6 -7
4 6

4
-8 6
-7 -1
-6 7
-1 3
'''


# 누전차단기 위치는 (0, 0)으로 입력으로 안 주어짐

T = int(input())
for tc in range(1, T+1):

    N = int(input()) # 콘센트의 갯수
    # N = 4
    consent = [[0, 0]]
    for _ in range(N):
        consent.append(list(map(int, input().split())))
    # print(consent)

    # 그렇다면 이제 인접 리스트 만들어주자,, 전부 인접해있다고 가정할거임,,
    # 이 길이들을 가중치로 두면 되겠지

    graph = [[] for _ in range(N + 1)]

    for i in range(N + 1): # 나는 누전차단기부터 세줄거니깐 ㅇㅇ
        for j in range(N + 1):
            if i == j:
                continue
            dist_ij = eleclinelen(consent[i], consent[j])
            graph[i].append((dist_ij, j))

    # print(graph)

    # graph = [
    #     [(7, 1), (12, 2), (10, 3), (13, 4)],
    #     [(7, 0), (5, 2), (3, 3), (6, 4)],
    #     [(12, 0), (5, 1), (2, 3), (3, 4)],
    #     [(10, 0), (3, 1), (2, 2), (3, 4)],
    #     [(13, 0), (6, 1), (3, 2), (3, 3)]]

    # graph = [
    #     [(7, 1)],
    #     [(7, 0), (5, 2), (3, 3), (6, 4)],
    #     [ (5, 1), (2, 3), (3, 4)],
    #     [ (3, 1), (2, 2), (3, 4)],
    #     [ (6, 1), (3, 2), (3, 3)]]
    # 모든 위치에 대해 가중치를 가지는 그래프 완성 # 자기 자신 제외


    # 이제 그냥 다익스트라 돌리자
    #
    # pq = [(0, 0), (3, 4), (1, 10)] # 시작 노드

    # pq = heapq.

    # pq = [(2, 3), (3, 4), (1, 3), (1, 1)]
    # now_node = heapq.heappop(pq)
    # print(now_node)
    inf = float('inf')
    # dist = [(inf, i) for i in range(N+1)]
    dist = [inf] * (N + 1)
    # heapq.
    pq = [(0, 0)]
    linked = 0
    while pq:
        now_info = heapq.heappop(pq)
        now_dist = now_info[0]
        now_node = now_info[1]

        linked += 1
        # 만약 지금 뽑아낸 거리가 누적거리보다 이미 길다면 패스
        # if now_dist >= dist[now_node][0]:
        if now_dist >= dist[now_node]:
            continue
        # 아니라면 배열에 최소누적거리를 저장해줘야겠징
        # dist[now_node] = (now_dist, linked)
        dist[now_node] = now_dist

        # 그럼 여기서 탐색 가능한 다음 애들을 찾아줄까??
        for next_info in graph[now_node]:
            next_dist = next_info[0]
            next_node = next_info[1]
            # if next_dist >= dist[next_node][0]:
            if next_dist >= dist[next_node]:
                continue
            new_dist = now_dist + next_dist
            heapq.heappush(pq, (new_dist, next_node))


    # print(dist) # [0, 7, 12, 10, 13]
    print(f"#{tc} {dist[N]}")
# 하.. 근데 이거 배선의 전선의 길이 구하는 거랑은... 조금 차이가 잇음.. 0부터 가는 최소거리이기때문에,,,
# 다익이는 순환에서 못쓴다는걸,, 내가 ,, 처리를,, 못햇네,,
# 이거 방문처리로 단방향 만들어야 하나? 근데 그게 가능한가? 누적거리의 개념 상 이건 불가능할거같은디
# 걍 지금이라도 BFS 돌려??


# BFS()

# [(0, 0), (7, 4), (12, 10), (10, 7), (13, 13)]
# [(0, 1), (7, 2), (12, 5), (10, 3), (13, 9)]