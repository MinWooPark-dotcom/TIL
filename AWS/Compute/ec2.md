# EC2(Elastic Compute Cloud)

## 가격 모델
| 요금 모델                | 특징                                                     | 주요 사용 사례                                |
| -------------------- | ------------------------------------------------------ | --------------------------------------- |
| On-Demand            | 예약 없이 시간 단위 과금<br>최대 유연성, 비용 가장 높음                     | 단기 테스트, 예상치 못한 워크로드, 초기 개발 단계           |
| Reserved (RI)        | 1년 또는 3년 단위로 예약, 최대 75% 할인<br>Standard, Convertible 유형 | 장기 워크로드, 항상 실행되는 서비스 (예: 웹 서버, DB 서버 등) |
| Spot                 | 미사용 EC2 자원을 경매식으로 저렴하게 구매<br>최대 90% 절약                 | 배치 작업, 테스트, 비핵심 서비스, 중단 가능 워크로드         |
| Savings Plan         | 컴퓨팅 사용량(\$/hr) 기준으로 할인 적용<br>RI보다 유연함                  | 여러 인스턴스 종류/VPC/리전 간 자유롭게 이동 가능 시        |
| Dedicated Host       | 물리 서버 단위로 예약, 라이선싱 제어 필요 시 사용                          | BYOL(Bring Your Own License) 시나리오 등     |
| Capacity Reservation | 특정 AZ에서 용량을 미리 확보, 추가 비용 없음                            | 가용성 중요 서비스에 사용 (재해 복구, 장애 대비)           |

| 항목          | On-Demand | Reserved Instances | Spot         | Savings Plan |
| ----------- | --------- | ------------------ | ------------ | ------------ |
| 약정 필요 여부    | ❌         | ✅ 1년 / 3년          | ❌            | ✅ 1년 / 3년    |
| 할인율         | -         | 최대 75%             | 최대 90%       | 최대 72%       |
| 중도 해지 가능 여부 | O         | ❌                  | O            | ❌            |
| 사용 유연성      | 최고        | 낮음 (인스턴스 타입 고정)    | 중간 (중단 가능)   | 높음 (유형 유연함)  |
| 대표 사용 사례    | PoC, 테스트  | 웹서버, DB 등 상시 서비스   | 배치 작업, 캐시 서버 | 다이나믹한 워크로드   |

- EC2 인스턴스 요금은 워크로드 특성에 따라 On-Demand / RI / Spot / Savings Plan 등으로 나뉨
- RI(예약형) + Spot(배치 작업) 조합이 가장 많이 사용됨
- Savings Plan은 인스턴스 변경이 자주 필요한 경우 RI보다 더 유연함
- 인스턴스의 중단 가능 여부, 실행 시간, 예측 가능성을 기준으로 전략을 짜야 함
- 비용 최적화를 위해 On-Demand + Spot 인스턴스 혼합 사용 시에는 Launch Configuration 사용은 불가하고 Launch Template만 사용 가능함

## 배치 그룹(Placement Group)
EC2 인스턴스의 물리적 배치 전략을 지정하는 기능
고성능 컴퓨팅, 고가용성, 네트워크 지연 최소화 등 특정 목적에 따라 인스턴스를 어떻게 "가까이" 또는 "분산" 배치할지를 정함.
Cluster, Partition, Spread 유형이 있음.

### Cluster
- 인스턴스를 물리적으로 가까운 호스트에 배치해서 낮은 지연과 고속 네트워크 성능 확보
- 고성능 컴퓨팅(HPC), Spark, Hadoop이 있음

### Partition
- 인스턴스를 논리적으로 그룹을 나누어 서로 다른 물리적 하드웨어에 배치, 장애 도메인과 격리 가능
- 대규모 Hadoop, HDFS, Cassandra 등이 있음

### Spread
- 인스턴스를 가능한 서로 다른 하드웨어에 광범위하게 분산 배치하여 최대 장애 격리 가능
- 소규모 고가용성 워크로드 (e.g. 7개 이하)

## 인스턴스 접근 제어
EC2 인스턴스에 대한 외부 접속은 보안 그룹(Security Group)과 네트워크 Access Control(Network ACL) 설정을 함께 확인해야 함.
### Security Group(SG)
- Stateful(상태 저장) 방화벽
- Inbound 규칙만 설정하면 아웃바운드 트래픽은 자동 허용됨(아웃바운드의 경우 특별한 상황이 아니라면 0.0.0.0/0으로 모두 허용)
- EC2 인스턴스 단위로 적용됨
- 허용만 가능(Deny 불가)

### Network ACL(NACL)
- Stateless(상태 비저장) 방화벽
- 인바운드와 아웃바운드 트래픽을 별도로 모두 허용해야 통신 가능
- 서브넷 단위로 적용됨
- Allow/Deny 모두 가능
- IP 차단, 서브넷 차원의 공통 정책 등이 필요할 때 사용

## Volume
### Solid State Drive(SSD)
Solid state drive (SSD) backed volumes optimized for transactional workloads involving frequent read/write operations with small I/O size, where the dominant performance attribute is IOPS.
can be used as a boot volume.
- General Purpose SSD (gp2)
- Provisioned IOPS SSD (io1)
- Instance Store

### Hard disk Drive(HDD)
Hard disk drive (HDD) backed volumes optimized for large streaming workloads where throughput (measured in MiB/s) is a better performance measure than IOPS.
 CANNOT be used as a boot volume
- Throughput Optimized HDD (st1)
- Cold HDD (sc1) volume types

## Reference
[Instance store temporary block storage for EC2 instances
](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Instance33Storage.html)