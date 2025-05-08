# IAM(Identity and Access Management)

## 교차 계정 액세스 활성화
- 여러 AWS 계정을 사용하여 비즈니스 애플리케이션과 데이터를 격리하고 관리하는 것이 좋습니다.
- 한 AWS 계정의 ID가 다른 AWS 계정의 리소스에 액세스하도록 허용하려면 IAM 역할을 사용하여 액세스를 제공할 수 있습니다.
- IAM 역할을 사용하면 일반적으로 조직의 AWS 리소스에 액세스할 수 없는 사용자 또는 서비스에 액세스 권한을 위임할 수 있습니다. 
- IAM 사용자 또는 AWS 서비스는 AWS API 호출에 사용할 수 있는 임시 보안 자격 증명을 얻는 역할을 맡을 수 있습니다. - 따라서 리소스에 액세스하기 위해 장기 자격 증명을 공유할 필요가 없습니다.

## Reference:
- [IAM 역할 관리](https://aws.amazon.com/ko/iam/features/manage-roles/)