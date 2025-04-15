# 모델 성능 평가 지표

## F1 스코어 (F1 Score)

- **정의**:
  - 정밀도(Precision)와 재현율(Recall)을 균형 있게 평가하기 위한 F-measure의 특수한 형태로, β=1일 때 사용됩니다.
  - F-measure는 분류 모델(classifier)이 얼마나 잘 분류했는지를 평가하는 지표 중 하나로, **정밀도와 재현율을 결합하여 하나의 수치로 종합적인 성능을 평가**할 수 있게 합니다.
  - 이 지표는 두 값의 **조화 평균(harmonic mean)** 을 기반으로 하며, F1 Score는 **정밀도와 재현율을 동등하게 중요하게 여길 때(β=1)** 사용하는 대표적인 방식입니다.

- **적합한 상황**:   
  - 불균형 데이터셋에서 정확도(Accuracy)가 왜곡될 때, 특히 소수 클래스의 성능 평가가 중요한 문제인 상황에 적합합니다.
  
- **예시**:  
  - 이진 분류 문제 (스팸 메일)
    - 정상 메일이 9,500개
    - 스팸 메일이 500개
    - 전체 10,000개의 데이터 중 95%가 정상
    - 만약 모델이 "전부 정상 메일이다"라고만 예측해도 정확도 95%
    - 하지만 "스팸 메일"은 거의 못 맞추는 모델
    - 이런 경우, 정확도(Accuracy)는 높아도 성능이 나쁜 모델
    - 스팸 메일(소수 클래스)을 놓치지 않으면서도, 정상 메일을 잘못 스팸으로 분류하지 않도록 정밀도와 재현율 사이의 균형이 중요할 때 F1 Score를 사용합니다.

- **추가 참고**:   
  - F<sub>β</sub> score = (1+<sub>β</sub>) * (Precision * Recall) / (Precision + Recall)
  - β (베타)는 "재현율(Recall)이 얼마나 더 중요한가?"를 나타내는 가중치 조절 파라미터
    - β = 1: 정밀도와 재현율을 동등하게 평가 → F1 Score
    - β > 1: 재현율(Recall)을 더 중요하게 평가 -> e.g. F<sub>2</sub>	Score
    - β < 1: 정밀도(Precision)를 더 중요하게 평가 -> e.g. F<sub>0.5</sub>	Score
  - F1 score:  F1 = 2 * (Precision * Recall) / (Precision + Recall) = 2 * (정밀도 * 재현율) / (정밀도 + 재현율)
  - F1 Score가 높다 → 정밀도와 재현율이 모두 높다
  - F1 Score가 낮다 → 둘 중 하나라도 낮음 → 모델의 실제 활용 성능이 떨어질 수 있음
  - 최소 0, 최대 1의 값을 가지며, F1 Score가 높다는 건 Precision과 Recall 모두 일정 수준 이상이라는 뜻이며 둘 중 하나라도 낮으면 F1 Score는 낮아짐.   
  - 정밀도(Precision): 모델이 True라고 분류한 것 중에서 실제 True인 것의 비율, positive predictive value(PPV)로 불리기도 합니다.
    - Precision = tp(True Positive) / tp(True Positive) + fp(False Positive)
  - 재현율(Recall): 실제 True인 것 중에서 모델이 True라고 예측한 것의 비율, sensitivity로도 불립니다.
    - Recall = tp(True Positive) / tp(True Positive) + fn(False Negative)
  - 조화 평균(Harmonic Mean): 여러 수의 역수(1/값)의 평균을 다시 역수로 취한 값입니다. 
    - 평균 내는 방식 중 하나, 값들이 균형을 이루는 쪽에 더 민감하게 반응.
    - 작은 값의 영향을 크게 반영해서 균형을 잘 평가하는 평균
    - 수식: H = 2xy / x + y
  
- Reference:
  - [F-score](https://en.wikipedia.org/wiki/F-score)
  - [조화 평균](https://ko.wikipedia.org/wiki/%EC%A1%B0%ED%99%94_%ED%8F%89%EA%B7%A0)
  - [정밀도와 재현율](https://ko.wikipedia.org/wiki/%EC%A0%95%EB%B0%80%EB%8F%84%EC%99%80_%EC%9E%AC%ED%98%84%EC%9C%A8)