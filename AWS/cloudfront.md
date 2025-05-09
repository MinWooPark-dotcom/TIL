# Amazon CloudFront 활용과 설계
## 개념 요약
- CloudFront는 AWS의 글로벌 CDN(Content Delivery Network) 서비스
- 정적 리소스뿐 아니라 동적 콘텐츠(조건부 캐싱), API 응답도 캐싱 및 라우팅 가능
    - Cache-Control 헤더, 쿼리/쿠키/헤더 포함 여부, Cache Policy등을 통해 동적 콘텐츠 캐싱이 가능
- 글로벌 엣지 로케이션을 통해 사용자 요청을 가장 가까운 곳에서 처리

## 아키텍처 흐름 예시
### 시나리오
- 미국에 있는 EC2 또는 ALB 백엔드 서버
- 한국 사용자 대상 신규 서비스 론칭
- 백엔드는 그대로 두고, 사용자 응답 속도만 빠르게 하고 싶음
### 아키텍처
사용자(한국) → CloudFront(서울 엣지 로케이션) → 백엔드(ALB, 미국)
- CloudFront를 사용해서 사용자와 가까운 엣지 로케이션을 활용하면, 백엔드를 유지하면서도 레이턴시를 줄일 수 있음
- CloudFront는 DNS 이름(e.g. `d1234.cloudfront.net`)을 통해 글로벌 접속 처리
- 정적 리소스는 엣지에서 캐시되므로 빠르게 응답
- 동적 API는 미국으로 전달되지만, TLS 핸드셰이크 및 DNS 지연은 줄어듦
    - 엣지 로케이션에서 TLS 핸드셰이크를 대신 처리함, 사용자 - CloudFront 엣지 간 TLS 연결만 맺어 백엔드까지 갈 필요가 없어서 레이턴시가 감소 됨.
    - Anycast IP(같은 IP를 전 세계에 퍼뜨려서 요청자가 가장 가까운 노드로 자동 라우팅), DNS 캐시, TTL 최적화 등 전 세계 DNS 최적화된 구조를 가졌기에 엣지 로케이션으로 자동 라우팅 됨.

## 적용 포인트
| 항목 | 내용 |
|------|------|
| 정적 콘텐츠 | HTML, JS, CSS, 이미지 → 캐시하여 속도 향상 |
| 동적 콘텐츠 | 쿠키, 쿼리스트링 기반 요청 → 원본에 전달하되, 엣지 최적화 가능 |
| 실시간 무효화 | 객체 변경 시 `invalidation` 사용 |
| 캐시 정책 | Cache-Control 헤더 기반 or CloudFront Behavior에서 수동 설정 |

## 자주 함께 쓰이는 서비스
- Route 53: 사용자 요청을 CloudFront로 보내는 DNS
- S3: 정적 사이트 호스팅 시 원본으로 사용
- WAF: CloudFront 레벨에서 글로벌 보안 제어
- Shield: DDoS 보호 (CloudFront, ALB, Route 53등 사용 시 자동으로 제공)