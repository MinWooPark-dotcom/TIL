# Kinesis

## 기본 개념
- 실시간 스트리밍 데이터를 수집, 처리 및 분석하여 적시에 인사이트를 확보하고 새로운 정보에 신속하게 대응할 수 있습니다.
- 기계 학습, 분석 및 기타 애플리케이션을 위해 비디오, 오디오, 애플리케이션 로그, 웹 사이트 클릭스트림 및 IoT 텔레메트리 데이터와 같은 실시간 데이터를 수집합니다.
- 모든 데이터가 수집된 후에야 처리를 시작할 수 있는 것이 아니라 데이터가 수신되는 대로 처리 및 분석하고 즉시 대응할 수 있습니다.

## 사용 사례
- 비디오 분석 애플리케이션 구축
    -  가정 및 공공 장소에 있는 카메라 장착 디바이스에서 AWS로 동영상을 안전하게 스트리밍하고 보안 모니터링, 얼굴 탐지 및 기타 분석에 이 비디오 스트림을 사용합니다.
- 배치에서 실시간 분석으로 발전
    - 기존에 배치 처리를 사용하여 분석하던 데이터에 대해 실시간 분석을 수행할 수 있습니다. 예를 들어 여러 애플리케이션 간에 데이터를 공유하고 ETL(Extract-Transform-Load)을 스트리밍하는 것입니다
- 실시간 애플리케이션 구축
    - 애플리케이션 모니터링, 사기 탐지, 실시간 순위표와 같은 실시간 애플리케이션에 Kinesis를 사용하여 고객과 애플리케이션이 현재 무엇을 하고 있는지 파악하고 즉시 대응할 수 있습니다.
- IoT 디바이스 데이터 분석
    - IoT 디바이스에서 스트리밍 데이터를 처리하고 해당 데이터를 사용하여 실시간 알림을 보내거나 센서가 특정 작동 임계값을 초과할 경우 프로그래밍 방식으로 기타 조치를 취합니다.

## Kinesis 서비스
Kinesis (실시간 스트리밍 플랫폼)
├── Kinesis Data Streams (KDS) ← 직접 쓴다 / 분석한다
├── Kinesis Data Firehose (KDF) ← 목적지로 보낸다
├── Kinesis Data Analytics (KDA) ← SQL로 분석한다
└── Kinesis Video Streams (KVS) ← 영상 데이터 처리

| 서비스 이름                     | 줄임말 | 주요 목적                             |
| -------------------------- | --- | --------------------------------- |
| **Kinesis Data Streams**   | KDS | 데이터 스트리밍 처리 (실시간 분석 등)            |
| **Kinesis Data Firehose**  | KDF | 실시간 데이터를 저장소로 전송 (S3, Redshift 등) |
| **Kinesis Video Streams**  | KVS | 비디오 데이터 전송 및 분석                   |
| **Kinesis Data Analytics** | KDA | KDS나 KDF로 받은 데이터를 SQL로 분석         |

- Kinesis Firehose는 2가지 입력 방식 중 하나만 가능:
  1. PutRecord / PutRecordBatch (직접 입력)
  2. Kinesis Data Stream(KDS)를 source로 지정

- Firehose가 KDS를 source로 쓰면, **직접 PutRecord는 비활성화됨**
- Kinesis Agent는 Firehose로 직접 쓰지 못하고, **KDS로 보내야 정상 작동**

## Reference
- [서버리스 스트리밍 데이터 서비스 - Amazon Kinesis](https://aws.amazon.com/ko/pm/kinesis/?trk=5860e0a8-c230-4101-ba35-cdf15ec7e186&sc_channel=ps&ef_id=Cj0KCQjww-HABhCGARIsALLO6Xxl-1aKOtzLmqe0To9IGM5dCiYs9J0ikkurv3_k33BMredLAa_keDkaAgqyEALw_wcB:G:s&s_kwcid=AL!4422!3!651510601836!p!!g!!kinesis%20stream!19828229715!148480174473&gad_campaignid=19828229715&gbraid=0AAAAADjHtp-nVczWWxUAzkjn5KApejfsF&gclid=Cj0KCQjww-HABhCGARIsALLO6Xxl-1aKOtzLmqe0To9IGM5dCiYs9J0ikkurv3_k33BMredLAa_keDkaAgqyEALw_wcB)