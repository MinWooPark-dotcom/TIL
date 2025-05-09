# Resource 관리

%CPU/R이 100% 넘으면 -> Request 조정
Request = 최소 보장 리소스
- Request는 스케줄링에 사용
- 이 값은 노드에 파드를 배치할 때, 이만큼은 반드시 보장해줘야 한다고 k8s에 알려주는 값
- k8s는 노드에 리소스가 충분할 때 배치하니까, Request가 작으면 작은 노드에도 많이 배치될 수 있음.

문제
- 파드가 실제로 Request 이상을 자주 사용하면?
    - 자주 CPU가 모자라서 성능 저하
    - 오토스케일링 트리거도 부정확할 수 있음
    - 스케줄링 시 적절한 리소스를 가진 노드에 배치 안 될 위험

Request 조정 이유
- 실제 필요한 최소 리소스를 정확히 알려주면
    - 적절한 노드에 배치되고
    - 자원 경합 줄이고
    - 클러스터 자원 효율적으로 사용 가능

%CPU/L이 100%에 가까우면 -> 왜 Limit 조정?
Limit = 최대 허용 리소스
- 파드는 Limit 이상 리소스를 절대 못 씀
- CPU는 쓰로틀링되고 메모리는 killed 될 수 있음

문제
- Limit에 자주 도달하면?
    - CPU 쓰로틀링 -> 성능 저하
    - 메모리 초과 -> OOMKilled -> 파드 재시작
- 이건 사용자가 파드를 쓸 수 있는 최대치를 너무 작게 잡아서 생기는 문제

Limit 조정 이유
- 파드가 실제로 필요로 하는 최대 사용량을 반영해 Limit을 늘리면
    - 성능 저하 방지
    - 불필요한 재시작 방지
    - 서비스 안정성 증가

Reuqest: 파드가 최소 이만큼 필요하니 잘 배치해줘!
Limit: 파드가 최대 이만큼만 쓰게 할게. 넘으면 강제 제한할거야!
