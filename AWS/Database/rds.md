# RDS

## Primary-Replica Architecture
- 시스템 규모가 커질수록 Read 요청의 비중이 증가하고, 이로 인해 Write 성능까지 저하되는 병목 현상이 발생할 수 있다.
- 이를 해결하기 위한 대표적인 접근 방식 중 하나가 Read Replica 구성이다.
- Read Replica
    - 쓰기 가능한 Primary 데이터베이스의 데이터를 복제한 읽기 전용 Replica 인스턴스이다.
    - 대부분의 시스템에서 복제는 비동기적으로 수행되며, replication lag이 발생할 수 있다.
    - 읽기 요청은 Replica에서 처리하고, 쓰기 요청은 Primary에서 처리하도록 애플리케이션을 구성한다.
- 읽기/쓰기 분리
    - 읽기 쿼리(SELECT)는 Replica, 쓰기 쿼리(INSERT, UPDATE, DELETE)는 Primary로 전송되도록 분리한다.
- Failover 구성
    - Primary 인스턴스에 장애가 발생했을 때, Replica 중 하나를 승격하여 새로운 Primary로 전환한다.
    - Auto Failover를 지원하는 시스템을 사용할 수도 있고, 수동 전환을 통해 직접 조치하는 방식도 있다.
- Replica 로드밸런싱
    - 여러 개의 Read Replica를 구성하면 읽기 트래픽을 분산할 수 있다.