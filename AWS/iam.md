# IAM(Identity and Access Management) 활용과 설계

## 개념 요약
- IAM은 AWS 리소스에 대한 접근 제어 및 권한 위임을 관리하는 핵심 서비스
- 사용자(User), 역할(Role), 그룹(Group), 정책(Policy) 등을 통해 세분화된 보안 통제 구현
- 정책은 JSON 형식의 권한 선언문이며, 허용/거부(Allow/Deny) 규칙을 정의

## 아키텍처 흐름 예시
### 시나리오
- 한 SaaS 기업이 DevOps 계정, 운영 계정, 로그 수집 계정 등 계정 분리 아키텍처(AWS Organizations)를 채택
- DevOps 팀은 CI/CD 파이프라인을 통해 운영 계정의 EKS, RDS, S3에 접근해야 함
- 보안팀은 DevOps 팀이 IAM 역할을 생성하거나 Assume할 수는 있지만, 과도한 권한 부여를 제한해야 함

### 아키텍처 구성: 조직 기반 권한 위임 아키텍처
[개발자] 
  → [DevOps 계정의 CI/CD 파이프라인]
    → IAM Role (AssumeRole)
      → [운영 계정의 리소스 접근: EKS, RDS, S3]

- Permissions Boundary
    - DevOps 계정 내 IAM 역할 생성 시, 최대 권한의 상한선을 설정해 오버 프로비저닝 방지
- Cross-account Role + Trust Policy
    - 운영 계정에서 역할을 생성하고, DevOps 계정에서 AssumeRole 가능하도록 신뢰 정책(Trust Policy) 구성
- Least Privilege Policy
    - 접근 대상 리소스(EKS, RDS, S3)에 필요한 최소 권한만 부여하여 보안 최소화 원칙 적용
- CloudTrail + IAM Access Analyzer
    - 누가 어떤 역할을 Assume했는지 감사하고, 퍼블릭/외부 접근 가능성 분석

## 적용 포인트
| 기능                    | 설명                        | 적용 예시                                   |
| --------------------- | ------------------------- | ------------------------------------------ |
| IAM Role              | 사람 or 서비스가 맡는 "임시 권한 역할"  | Lambda, ECS Task, CodeBuild 등에서 역할로 리소스 접근 |
| Trust Policy          | 어떤 주체가 이 역할을 사용할 수 있는지 정의 | cross-account 접근 제어                        |
| Permissions Boundary  | 권한 상한선 제한                 | 내부 팀이 IAM 역할을 만들 때 권한 오버로드 방지              |
| Resource-based Policy | 리소스 쪽에서 접근을 허용            | S3 버킷, SNS, SQS 등에 붙임                      |
| IAM Policy Simulator  | 정책 시뮬레이션 도구               | "이 유저가 이 액션 가능해?" 빠르게 확인                   |

IAM Role vs IAM User 구분해서 사용해야 하는 타이밍
- 사용자(User): 사람 계정, 콘솔 로그인 필요할 때
- 역할(Role): 서비스, 임시 권한, 또는 cross-account 접근 시
- 서비스 = Role, 사람 = User or SSO
    - Single Sign-On란 하나의 계정으로 여러 시스템에 공통 인증을 가능하게 하는 통합 로그인 시스템
    - 조직 사용자들이 외부 인증 기반으로 AWS에 로그인하고 역할 Assume 가능
    - 즉, AWS Organizations 내 여러 계정의 IAM Role을 Assume 가능

Cross-account 접근에 버킷 정책이 필요한 이유
- IAM Role은 주체(Principal)에 권한 부여
- 리소스(S3 등)는 정책으로 접근 허용 여부를 따로 판단
- 서로 다른 계정이면 IAM 정책 + 리소스 정책 둘 다 있어야 허용

Permissions Boundary이 필요한 시점
- 하위 관리자(DevOps팀 등)가 IAM Role을 생성할 수 있도록 할 때
- 단, 권한을 ec2:*, iam:*처럼 과도하게 줄 경우를 방지하기 위해 최대 범위 지정

## 권한 설계 상황별 사례
| 질문                                             | 사고 방향                                         |
| ---------------------------------------------- | --------------------------------------------- |
| “IAM 정책이 허용인데도 요청이 실패하는 경우는?”                  | 리소스 정책에서 거부(Deny), SCP 영향, 권한 부족 등            |
| “IAM 사용자와 역할이 같은 정책을 가졌다면 차이는?”                | 역할은 임시, AssumeRole 필요. 사용자는 바로 로그인 가능         |
| “Lambda가 다른 계정의 S3 접근할 때 필요한 설정은?”             | Lambda 실행 Role + S3 Bucket Policy 모두 필요       |
| “다수의 팀이 IAM 역할을 만들 수 있도록 하되, 실수나 권한 남용을 막으려면?” | Permissions Boundary 적용 필요                    |
| “IAM 정책과 Resource Policy, SCP의 적용 우선순위는?”      | 명시적 Deny > SCP > Resource Policy > IAM Policy |


## 자주 함께 쓰이는 서비스
- CloudTrail: 누가 어떤 IAM 액션을 했는지 로깅
- IAM Access Analyzer: 퍼블릭/외부 접근 가능한 리소스 식별
- AWS Organizations + SCP: 계정 레벨 정책 제어
- STS: AssumeRole을 통한 임시 자격 증명 제공

