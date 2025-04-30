# DNS 질의 흐름

### 1. 브라우저 → OS → **Local DNS Resolver**에 질의

- 질문자: 브라우저는 OS의 DNS Client(Stub Resolver)에게 요청하고, OS는 Local DNS Resolver에게 질의한다.
- 질의 대상: **Local DNS Resolver** (예: 8.8.8.8, 1.1.1.1, ISP DNS)
- 질의 내용: A record for [api.www.example.com](http://api.www.example.com/).

### 2. Local DNS Resolver (예: 8.8.8.8)에서 **캐시 조회**

- **있으면 바로 응답하고 끝**
- **없으면 다음 단계 수행**

### 3. Local DNS Resolver → **Root DNS 서버에 질의**

- 질문자: 로컬 리졸버
- 질의 대상: Root DNS 서버
- 질의 내용: A record for [api.www.example.com](http://api.www.example.com/).
    - 항상 전체 도메인 이름(api.www.example.com)으로 질의
- 응답 내용:
    - 응답은 **그 도메인을 직접 알지 못하므로 상위 도메인의 NS만 알려주는 것**
    - Root는 IP는 모름
    - 대신 `.com.` 도메인을 담당하는 **TLD 네임서버의 NS 레코드**를 응답
    - 예시 응답:
        
        ```
        ;; AUTHORITY SECTION:
        com.    172800  IN  NS  [a.gtld-servers.net](http://a.gtld-servers.net/).
        com.    172800  IN  NS  [b.gtld-servers.net](http://b.gtld-servers.net/).
        
        ;; ADDITIONAL SECTION:
        [a.gtld-servers.net](http://a.gtld-servers.net/).  172800  IN  A   192.5.6.30
        ```
        
    - .com.에 대한 NS 레코드 + 그 중 일부의 IP 주소(A 레코드) 도 같이 응답
    - `ADDITIONAL SECTION`의 A 레코드는 **필수는 아님,** 어떤 루트/네임서버는 NS만 줄 수 있음
    - e.g., NS for `.com.` (예: `a.gtld-servers.net.` + IP)

### 4. Local DNS Resolver → TLD DNS 서버 (예: `192.5.6.30`)에 질의

- 질문자: 로컬 리졸버
- 질의 대상: TLD DNS 서버
- 질의 내용: A record for [api.www.example.com](http://api.www.example.com/).
    - 항상 전체 도메인 이름(api.www.example.com)으로 질의
- 응답 내용
    - 응답은 **그 도메인을 직접 알지 못하므로 상위 도메인의 NS만 알려주는 것**
    - `TLD DNS 서버`는 `example.com.`에 대한 **NS 레코드**만 알고 있음
    - 예시 응답:
        
        ```
        ;; AUTHORITY SECTION:
        example.com.   172800  IN  NS  ns1.exampledns.com.
        example.com.   172800  IN  NS  ns2.exampledns.com.
        
        ;; ADDITIONAL SECTION:
        ns1.exampledns.com.  172800  IN  A  203.0.113.10
        ```
        
    - `example.com.`을 관리하는 권한 네임서버(NS)의 도메인명과 IP를 알려줌
    - e.g. NS for `example.com.` (예: `ns1.exampledns.com.` + IP)

### 5. Local DNS Resolver → **`example.com.`의 권한 DNS 서버**(예: `203.0.113.10`)에 질의

- 질문자: 로컬 리졸버
- 질의 대상: SLD DNS 서버
- 질의 내용: A record for [api.www.example.com](http://api.www.example.com/).
- 응답 내용
    - 이 서버는 `example.com.`에 대한 권한을 갖고 있어, 하위 도메인인 `api.www.example.com`의 A 레코드를 직접 응답할 수 있음
    - 이 서버는 `example.com`의 하위 도메인에 대한 레코드를 관리함
    - 이 도메인이 실제로 설정돼 있다면 IP 반환
    - 예시 응답:
        
        ```
        ;; ANSWER SECTION:
        api.www.example.com.  300  IN  A  198.51.100.25
        ```
        
        - e.g. IP (예: 198.51.100.25)
- 최종 IP 주소 도착

### 6. Local DNS Resolver

- 받은 IP를 **브라우저에게 전달**
- 중간 얻은 `.com`, `example.com`의 NS, A 레코드 정보도 TTL 기준으로 **캐싱**

### 7. 브라우저 → TCP 연결 시도

```
GET / HTTP/1.1
Host: api.www.example.com
```

### 8. HTTP 요청/응답

### 9. 브라우저 렌더링