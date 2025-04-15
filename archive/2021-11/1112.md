# Today I Learned

매일 배운 것을 정리하며 기록합니다.
생활코딩 Docker 입문수업 강의를 통해 공부하였습니다.

---

## Docker란?

Docker가 무엇이고 왜 필요한지 이해하기 위해서 Docker의 사전적 의미를 먼저 이해하는 것이 도움이 됩니다.

Docker란 사전적 의미로 '부두 노동자'입니다.

부두 노동자는 부두에 정박해 있는 선박에 컨테이너를 싣고 나르는 일을 합니다.

컴퓨터 세상에서는 운영체제가 설치된 컴퓨터가 선박의 역할을 합니다.

운영체제가 설치된 컴퓨터는 주인이라는 의미에서 Host라고 합니다.

그 선박 안에 컨테이너를 실듯이 Host 컴퓨터 안에도 컨테이너를 실을 수 있습니다.

이러한 컨테이너는 각각의 실행 환경을 의미합니다.

각각의 Container에는 운영체제가 설치되어 있지 않고 App을 실행하기 위한 라이브러리와 실행 파일들만 포함되어 있습니다.

이렇듯 Host에 존재하는 운영체제를 공유하니 각 Container에서는 따로 운영체제를 설치할 필요도 없습니다.

덕분에 용량을 아끼며 빠른 속도로 사용이 가능합니다.

이러한 기술은 Docker만이 가진 기술은 아니며 Linux OS에 내장되어 있는 App 실행 방법입니다.

이를 Container라고 부릅니다.

Container 기술을 이용해서 이러한 일을 쉽게 해주는 소프트웨어 중 가장 잘 나가는 제품이 Docker인 것입니다.

---

## Image pull

![](https://images.velog.io/images/qmasem/post/03aecbec-0ebc-46e6-a73f-efc9b61b38bd/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-11-12%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%207.14.36.png)

iPhone에서 App을 설치할 때 App Store에서 찾고 설치한 것을 프로그램이라고 하고 프로그램을 실행하면 프로세스가 동작하는 것처럼,

Docker에서는 Docker Hub라고 불리는 Registry에서 필요한 소프트웨어를 다운로드하여 가지고 있는 것을 image라고 하며 이를 실행한 것을 container라고 합니다.

한 프로그램이 여러 개의 프로세스를 가질 수 있는 것처럼, image도 여러 개의 container를 가질 수 있습니다.

앱을 다운로드 받는 것처럼, Docker Hub에서 image를 다운로드 받는 행위를 Pull이라고 합니다.

image를 실행시키는 행위를 Run이라고 합니다.

### hub.docker.com 사용법

1. 먼저 Docker Hub의 주소인 https://hub.docker.com 에 접속합니다.

![](https://images.velog.io/images/qmasem/post/e32ae73d-f60d-403f-bddf-a043d2aabaf6/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-11-12%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%207.18.43.png)

2. 우측 상단에 Explore를 클릭합니다.

![](https://images.velog.io/images/qmasem/post/c5a92d66-0889-4c6b-8ea2-0aa2992961ce/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-11-12%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%207.20.09.png)

3. Pull 할 image를 선택 후 명령어와 설명을 확인합니다.

![](https://images.velog.io/images/qmasem/post/003a543a-871c-43eb-abb7-9948f7d356f3/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-11-12%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%207.23.57.png)

4. 터미널을 통해 Pull 합니다.

![](https://images.velog.io/images/qmasem/post/82fe60ea-0b25-4d69-908d-25600003ca1c/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-11-12%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%207.27.27.png)

5. `$ docker images` 명령어를 통해 Pull이 잘 되었는지 확인합니다.

![](https://images.velog.io/images/qmasem/post/e8d015f4-11c3-4b95-bbb3-2409ee48382d/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-11-12%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%207.27.54.png)

---

Reference :

생활코딩 Docker 입문수업 - 1.수업소개
생활코딩 Docker 입문수업 - 3. 이미지 pull
