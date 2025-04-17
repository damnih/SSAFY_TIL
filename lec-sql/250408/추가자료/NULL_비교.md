[toc]

# NULL 비교

>  SQL에서 NULL은 실제 값이 아니라 “값이 없음” 또는 “알 수 없음”을 의미합니다. 
>
> 때문에 일반적인 등호(`=`) 연산자로 NULL을 비교하면 의도한 대로 작동하지 않습니다.

## 1. SQL의 3값 논리

SQL은 논리 연산에 대해 세 가지 값을 사용합니다

- TRUE
- FALSE 
- UNKNOWN (알 수 없음)

예를 들어, `NULL = NULL`의 결과는 TRUE가 아니라 `UNKNOWN`이 됩니다. 

이는 두 NULL이 실제로 어떤 값을 가지고 있지 않기 때문입니다.



## 2. 값의 부재와 불확실성

- NULL은 “값이 존재하지 않음”을 나타내므로, 특정 값과 동일하다고 볼 수 없습니다.
- `=` 연산자를 사용하면, NULL은 어떤 값과도 비교할 수 없으므로 결과가 UNKNOWN이 되어 기대한 결과를 얻지 못합니다.



## 3. 명시적 비교: IS와 IS NOT

- SQL 표준은 NULL 값을 비교할 때 명시적으로 IS NULL 또는 IS NOT NULL 구문을 사용하도록 규정합니다.
- WHERE column IS NULL은 해당 컬럼에 값이 없음을 정확하게 확인할 수 있도록 해줍니다.
- 반대로 WHERE column IS NOT NULL은 값이 존재하는 행을 찾습니다.



## 4. = 와 IS 비교

### 4.1 = 연산자

> 일반적인 값의 동등성(같음)을 비교할 때 사용합니다.

```sql
SELECT * FROM employees WHERE department = 'Sales';
```

- 제한사항
  - 만약 비교하는 값 중 하나라도 NULL이면, 결과는 UNKNOWN이 됩니다.
  - 예를 들어, NULL = NULL의 결과는 TRUE가 아니라 UNKNOWN입니다.
  - SQL의 3값 논리(참, 거짓, 알 수 없음) 체계 때문에 이런 결과가 발생합니다.

### 4.2 IS 연산자

> `NULL`과 같은 특별한 값을 비교할 때 사용

```sql
SELECT * FROM employees WHERE department IS NULL;
```

- 사용처

  1. NULL 비교

  2. Boolean 값 비교

     ```sql
     WHERE is_active IS TRUE
     ```

     

## 5. 정리

- NULL은 값의 부재를 나타내므로, 일반적인 = 연산자로 비교하면 3값 논리 체계에서 UNKNOWN이 반환되어 올바른 결과를 얻을 수 없습니다. 
- 따라서 SQL에서는 NULL을 비교할 때 IS 연산자를 사용합니다.
