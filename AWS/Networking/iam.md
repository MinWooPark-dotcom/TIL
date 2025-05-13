# IAM(Identity and Access Management) 활용과 설계

## 개념 요약

* IAM은 AWS 리소스에 대한 접근 제어 및 권한 위임을 관리하는 핵심 서비스
* 사용자(User), 역할(Role), 그룹(Group), 정책(Policy) 등을 통해 세분화된 보안 통제 구현
* 정책은 JSON 형식의 권한 선언문이며, 허용/거부(Allow/Deny) 규칙을 정의

## 아키텍처 흐름 예시

### 시나리오

* 한 SaaS 기업이 DevOps 계정, 운영 계정, 로그 수집 계정 등 계정 분리 아키텍처(AWS Organizations)를 채택
* DevOps 팀은 CI/CD 파이프라인을 통해 운영 계정의 EKS, RDS, S3에 접근해야 함
* 보안팀은 DevOps 팀이 IAM 역할을 생성하거나 Assume할 수는 있지만, 과도한 권한 부여를 제한해야 함

### 아키텍처 구성: 조직 기반 권한 위임 아키텍처

\[개발자]
→ \[DevOps 계정의 CI/CD 파이프라인]
→ IAM Role (AssumeRole)
→ \[운영 계정의 리소스 접근: EKS, RDS, S3]

## 핵심 구성 요소

* **Permissions Boundary**: DevOps 계정 내 IAM 역할 생성 시, 최대 권한의 상한선을 설정해 과도한 권한 부여 방지
* **Cross-account Role + Trust Policy**: 운영 계정에서 역할을 생성하고, DevOps 계정에서 AssumeRole 가능하도록 신뢰 정책 구성
* **Least Privilege Policy**: 접근 대상 리소스에 필요한 최소 권한만 부여
* **CloudTrail + IAM Access Analyzer**: 감사 및 외부 접근 가능성 분석
* **AssumeRole**: AWS에서 권한을 위임받아 다른 역할을 잠시 맡는 방식 (STS를 통해 실행)

## IAM 역할과 정책 적용 포인트

| 기능                    | 설명                  | 적용 예시                         |
| --------------------- | ------------------- | ----------------------------- |
| IAM Role              | 사람/서비스가 맡는 임시 권한 역할 | Lambda, ECS, CodeBuild 등에서 사용 |
| Trust Policy          | 역할 사용자를 지정하는 신뢰 정책  | Cross-account 접근 제어           |
| Permissions Boundary  | 권한 상한선 제한 도구        | DevOps팀의 IAM 역할 생성 제한         |
| Resource-based Policy | 리소스에서 접근 허용 정의      | S3, SNS, SQS 등                |
| IAM Policy Simulator  | 정책 시뮬레이션 도구         | 특정 액션 가능 여부 검증                |

## 상황별 권한 설계 사고 방식

| 질문                    | 사고 방향                                |
| --------------------- | ------------------------------------ |
| IAM 정책이 허용인데 요청 실패    | Resource Policy, SCP, 명시적 Deny 여부 확인 |
| 사용자와 역할이 같은 정책을 가졌다면? | 역할은 Assume 필요, 사용자는 직접 로그인 가능        |
| Lambda가 다른 계정 S3 접근   | 실행 Role + S3 Bucket Policy 필요        |
| DevOps 팀 권한 남용 방지     | Permissions Boundary 활용              |
| 정책 우선순위               | 명시적 Deny > SCP > 리소스 정책 > IAM 정책     |

## 자주 함께 쓰이는 서비스

* CloudTrail: IAM 활동 로깅
* IAM Access Analyzer: 퍼블릭 접근 리소스 탐지
* AWS Organizations + SCP: 계정 단위 제어 정책
* STS: AssumeRole을 통한 임시 자격 증명 발급


# Cross-Account IAM Role 실습: S3 접근 권한 위임

## 실습 목표

* Trusting Account에서 Trusted Account의 S3 버킷에 접근하도록 구성
* IAM Role Assume을 통해 교차 계정 권한 위임 구현

## 실습 절차 요약
1. Trusted Account: IAM Role 생성 및 Trust Policy 설정
2. Trusted Account: S3 버킷 생성 및 접근 권한 정책 구성
3. Trusting Account: IAM 사용자에게 AssumeRole 권한 부여
4. Trusting Account CLI: `sts:AssumeRole` 실행 후 임시 자격 증명 획득
5. Trusting Account: 임시 자격 증명을 환경 변수로 설정 후 S3 접근 확인

### 아키텍처 흐름
```
[Trusting Account IAM 사용자] 
      ↓ sts:AssumeRole
[Trusted Account IAM Role: CrossAccountS3AccessRole]
      ↓ 임시 자격 증명 발급
[S3 버킷: cross-account-bucket-for-test 접근 성공]
```

## 정책 구성 예시

### Trusted Account: IAM Role Trust Policy: 누가 이 역할을 맡을 수 있는가?

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::[A_ACCOUNT_ID]:root"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### Trusted Account: Role에 부여할 권한 정책: 이 역할이 맡으면 할 수 있는 권한

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::cross-account-bucket-for-test",
        "arn:aws:s3:::cross-account-bucket-for-test/*"
      ]
    }
  ]
}
```

### Trusting Account: IAM 사용자에 부여할 정책

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::[B_ACCOUNT_ID]:role/CrossAccountS3AccessRole"
    }
  ]
}
```
- 이 정책이 있어야 aws sts assume-role 명령이 성공함

## 실습 명령 예시

1. Trusted Account에서 S3 버킷 생성
- Public Access 차단 설정
- 버킷 안에 테스트로 확인할 파일 업로드

2. Trusted Account에서 IAM Role 생성 및 정책 추가

<img src="../images/IAM_role_creation_1.png"/>       
<img src="../images/IAM_role_creation_2.png"/>   
<img src="../images/IAM_role_permission_setting.png"/>

- Trusted Entity Type을 AWS Account 선택 후 Account ID에 Trusting Account의 AWS Account ID를 입력 후 생성 버튼 클릭
- Role 생성 후 Trsut relationships 확인하여 Principal.AWS의 값에 Trusting Account AWS Account ID가 잘 입력 되었는지, Action은 "sts:AssumeRole"이 설정되었는지 확인
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::330722768646:root"
            },
            "Action": "sts:AssumeRole",
            "Condition": {}
        }
    ]
}
```
- sts는 AWS Security Token Service로 역할을 Assume하거나 임시 자격 증명을 발급해 주는 서비스, Cross-account 권한 위임은 전부 sts를 통해 이뤄짐.
- sts는 AssumeRole(다른 역할을 맡기), GetSessionToken(임시 사용자 만들기), AssumeRoleWithWebIdentity(Cognito/OIDC 연계)를 담당
- Permission 탭에서 Create inline policy를 통해 다음 정책 추가
```
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "Statement1",
			"Effect": "Allow",
			"Action": [
			    "s3:ListBucket",
			    "s3:GetObject"
			],
			"Resource": [
			    "arn:aws:s3:::cross-account-bucket-for-test",
			    "arn:aws:s3:::cross-account-bucket-for-test/*"
			]
		}
	]
}
```

3. Trusting Account에서 AWS CLI로 AssumeRole 설정
<img src="../images/temporary_security_credentials.png"/>

```
aws sts assume-role \
  --role-arn arn:aws:iam::[B_ACCOUNT_ID]:role/[CROSS_ACCOUNT_S3_ACCESS_ROLE] \
  --role-session-name [STS_SESSION_NAME]
```
- IAM Role을 Assume하고 나면, 그 역할은 “그 계정 내의 정식 IAM 주체”처럼 행동 가능.
- 반환된 JSON에서 AccessKeyId, SecretAccessKey, SessionToken 추출

4. 임시 자격증명으로 환경 변수 설정
```
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...
```

5. S3 접근 테스트
<img src="../images/cross_account_s3_access_role_result.png"/>
```
aws s3 ls s3://cross-account-bucket-for-test
```