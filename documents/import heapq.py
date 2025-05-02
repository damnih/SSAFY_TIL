import heapq



# 일단 소모되는 연료의 값을 산출하는 식을 세워보자
def fuel(now, next):
    if now > next: # 나보다 다음이 작을 때 = 낮을 때
        cost = 0
    elif now == next:
        cost = 1
    elif now < next: # 나보다 다음 값이 클 때 = 높을 때
        cost = (next - now) * 2
    return cost



pq = [(0, 0)]
heapq.heapify(pq)




N = int(input())
map = [list(map(int, input().split())) for _ in range(N)]


INF = float('inf')

# print(43 < INF)

dist = [INF] * (N ** 2)
# dist_map = [[INF] * N for _ in range(N)]
# print(dist)
# print(dist_map)

dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

# now = heapq.heappop(pq)
# print(now)
# now_dist, now_node = now
# print(now_dist)
# print(now_node)
while pq:
    now = heapq.heappop(pq)
    # print(now)
    now_dist, now_node = now

    # 만약 지금 뽑아낸 거리가, 기존에 존재하던 거리의 최솟값보다 크다면, 무시해준다
    if dist[now_node] < now_dist:
        # dist[now_node] = now_dist
        continue
    if dist[now_node] > now_dist:
        dist[now_node] = now_dist
        # continue
    # 아니라면

    # 일단 이 뽑아낸 애의 인접한 애들을 탐색해줘
    # 인접한 애들은 어디에 어떻게 있다고?
    # 일단 뽑아낸 애의 좌표는
    now_r = now_node // N
    now_c = now_node % N

    # 현 좌표에 대해 델타탐색 ㄱㄱ = 인접한 녀석 탐색
    for sabang in range(4):
        next_r = now_r + dr[sabang]
        next_c = now_c + dc[sabang]
        # 벽 안에 있다면
        if 0 <= next_r < N and 0 <= next_c < N:
            # 제대로 골라준 거니깐 이 노드에 대해 이제 탐색 ㄱㄱ 할거임
            next_node = next_r * N + next_c
            # 이 노드까지의 가중치를 이제부터 계산해줄 거야
            next_height = map[next_r][next_c]
            now_height = map[now_r][now_c]
            # 이건 지금 노드부터 다음 노드까지의 거리임
            now_cost = fuel(now_height, next_height)

            # 그렇다면, 이제, 지금 노드와 다음 노드까지의 거리를 더해준 게, 다음 노드까지의 거리가 되겠다
            next_node_dist = now_dist + now_cost

            # 그렇다면 이제 이 다음 노드까지의 거리와 그 노드 번호를 힙에 넣어줄거임

            # 근데 이건 뭐랬어? 큐잖아? 넣기 전에 방문처리! 넣음과 동시에 방문처리를 하게 되는 거임
            # 그렇다면 넣음 = dist[next_node] = next_node_dist 라는 거네?
            # 근데 이 전에 하나 묻자,
            # 만약에 이거, 기존의 dist[next_node]가 지금 당장 계산해본 next_node_dist 보다 짧으면?? 굳이 이거 넣어줄 필요 있나?
            # 없지?
            # 그러니깐
            # next_node_dist 가 dis 보다 작을 때에 한해, 방문처리 해주고 dist 바꿔주면 될 것 같아!

            if next_node_dist >= dist[next_node]:
                continue
            dist[next_node] = next_node_dist
            heapq.heappush(pq, (next_node_dist, next_node))
            # print(pq)

            # (next_node_dist, next_node)
            # # if now의 dist와 now_cost를 더한 값이 dist[next]보다 작다면 dist를 갱신
            # if dist[next_node] > dist[now_node] + now_dist:
            #     total_next_dist = dist[now_node] + now_dist
            #     dist[next_node] = total_next_dist
            #     heapq.heappush(pq, (total_next_dist, next_node))


# print(dist)

# print(dist[N**2 - 1])

ans = dist[N**2 - 1]
print(f"# {ans}")