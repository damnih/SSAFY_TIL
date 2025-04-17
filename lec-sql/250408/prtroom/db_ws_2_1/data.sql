-- zoo.sqlite3 파일을 생성하여 데이터베이스로 사용한다.
-- data.sql 파일을 생성한다.
-- SQL문은 생성한 data.sql 파일에서 작성하고 실행한다.
-- 실행 방법
-- 각 요구사항에 적절한 SQL문을 작성한다.
-- 실행하고자 하는 SQL문을 우클릭한다.
-- Run Selected Query 를 선택하여 실행한다.
-- 결과를 확인한다.

DROP TABLE zoo; 

-- ERD를 참고하여 zoo.sqlite3에 zoo 테이블을 생성한다.
CREATE TABLE zoo (
  name TEXT NOT NULL DEFAULT 'default value',
  eat TEXT NOT NULL DEFAULT 'default value',
  weight INTEGER NOT NULL DEFAULT 'default value',
  height INTEGER NOT NULL DEFAULT 'default value',
  age INTEGER NOT NULL DEFAULT 'default value'
)

-- zoo 테이블에 최소 4개 이상의 데이터를 삽입한다.
INSERT INTO zoo (name, eat, weight, height, age)
-- INSERT INTO zoo -- 얘는 풀콤을 채워서 일케 컬럼명을 적어주지 않아도 ㅇㅋ 
VALUES 
('Lion', 'Meat', 200, 120, 5),
('Elephant', 'Plants', 5000, 300, 15),
('Giraffe', 'Leaves', 1500, 550, 10),
('Monkey', 'Fruits', 50, 60, 8);



-- zoo 테이블의 모든 데이터를 조회하여 출력한다.
SELECT * FROM zoo;