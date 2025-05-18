# AWS Direct Connect
- 온프레미스 네트워크와 AWS 간의 **전용 네트워크 연결**을 제공하는 서비스
- 공용 인터넷을 통하지 않고, 전용선을 통해 **안정적이고 빠른 전송**, **보안성 향상**, **지연 시간 최소화** 가능

## 구성 요소 및 개념

| 구성 요소                                    | 설명                                                                  |
| ---------------------------------------- | ------------------------------------------------------------------- |
| **Direct Connect**                       | 온프레미스 ↔ AWS 간 전용선 연결 서비스                                            |
| **Virtual Interface (VIF)**              | Direct Connect 상에서 논리적 연결을 설정하는 방식. Public, Private, Transit VIF 존재 |
| **Private VIF**                          | 온프레미스에서 VPC 내 리소스(EC2, EFS 등)에 Private IP를 통해 접근 가능              |
| **Public VIF**                           | 온프레미스에서 AWS의 퍼블릭 서비스(S3, DynamoDB 등)에 접근할 때 사용                      |
| **Transit VIF**                          | 여러 VPC와의 연결을 중앙집중형으로 구성할 때 사용 (Transit Gateway와 함께)                 |
| **Interface VPC Endpoint (PrivateLink)** | AWS 서비스(EFS, API Gateway 등)에 VPC 내부 사설 경로로 접근 가능하게 하는 엔드포인트     |

## 실습 시나리오 핵심 요약
온프레미스(NFS)에 저장된 파일을 AWS로 마이그레이션 전에 매일 Amazon EFS로 복사해야 하는 경우를 가정

### 해결 구성

```
[온프레미스 (NFS)] ← DataSync Agent
          ↓
[Direct Connect] + [Private VIF]
          ↓
[VPC Interface Endpoint (EFS API)]
          ↓
[Amazon EFS]
```

### 흐름 요약

- Direct Connect + Private VIF를 통해 VPC 내부로 사설 IP 기반 접근 가능
- VPC 내부에 Interface Endpoint(PrivateLink)를 만들어 **EFS API에 사설 IP로 접근 가능하게 구성**
- AWS DataSync는 Agent를 통해 NFS에서 파일을 읽고, 위 경로를 통해 EFS로 전송

## 핵심 이해 포인트

- **DataSync**: 실제 파일 복사 주체 (Agent 기반)
- **Direct Connect + Private VIF**: 트래픽 경로 (사설 통신, 고속/보안성 확보)
- **Interface Endpoint**: AWS 서비스에 사설 IP 기반 접근을 허용하는 VPC 내 도착지
- EC2, EFS, S3 등의 AWS 리소스에 **공용 IP 없이 온프레미스에서 직접 사설 통신**할 때 Direct Connect + Private VIF 조합을 사용
- EFS처럼 퍼블릭 API만 제공되는 서비스는 **PrivateLink 기반 VPC Endpoint**가 반드시 필요함

## 참고

* [https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html)
* [https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html](https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html)
