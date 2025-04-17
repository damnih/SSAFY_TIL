[toc]

# WHERE 와 HAVING

## 1. WHERE 절

- **목적**

  - 개별 행(row)에 대한 조건을 지정하여 데이터를 필터링합니다.

- **적용 시점**

  - **FROM**과 **JOIN** 등의 단계 이후, **GROUP BY** 이전에 적용됩니다.  


  

- **사용 예**

  - 특정 조건을 만족하는 행만을 대상으로 집계나 정렬 등의 작업을 수행할 때 사용합니다.

    ```sql
    SELECT *
    FROM employees
    WHERE salary > 30000;
    ```






## 2. HAVING 절 

- **목적**

  - **GROUP BY**에 의해 그룹화된 결과에 대해 조건을 지정하여 그룹을 필터링합니다.

- **적용 시점**

  - 그룹핑 및 집계(aggregate) 함수 적용 후에 조건을 평가합니다.

- **사용 예**

  -  그룹별 집계 결과에 조건을 걸어 특정 그룹만을 선택할 때 사용합니다.

    ```sql
    SELECT department, COUNT(*) AS num_employees
    FROM employees
    GROUP BY department
    HAVING num_employees > 5;
    ```




## 3. 정리

- **WHERE:** 개별 행을 대상으로 조건을 검사하여 필터링
- **HAVING:** 그룹핑된 결과(집계 결과)를 대상으로 조건을 검사하여 필터링

- WHERE 절은 집계 함수가 사용되기 전에 행을 필터링하고, 
  HAVING 절은 GROUP BY에 의해 만들어진 그룹에 대해 집계 함수나 그룹 기준으로 필터링하는 데 사용됩니다.