# Task Duplication

`fastapi` , `langchain`, `g4f` 라이브러리를 동시에 실행하는 과정에서 task가 중복실행되어 텍스트 generation이 안되는 현상이 발생

```
Cannot enter into task
```

이를 해결하기 위해서는 **g4f 라이브러리의 Provider 중 비동기가 아닌 동기로 generation 하는 Provider**를 선택해야함

또한 `langchain` 의 callbacks를 `LLMChain`이 아닌, 실행시키는 인자, 즉 `arun()` 메서드안의 파라미터로 넣어야 함
