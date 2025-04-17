
DROP TABLE orders;

PRAGMA table_info('orders');
PRAGMA table_info('customers');

-- orders 테이블을 생성한다. 상세한 schema는 첨부 파일 참고.
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
  order_date DATE NOT NULL,
  total_amount REAL NOT NULL
)

-- orders 테이블에 서로 다른 데이터를 최소 3개 이상 삽입한다.
-- Date 타입은 'YYYY-MM-DD' 형식으로 삽입한다.
-- Real 타입은 10.11 형식으로 삽입 가능하다.
INSERT INTO orders (order_date, total_amount)
VALUES ('2023-07-15', '50.99'),('2023-07-16', '75.5'), ('2023-07-17', '30.25');



-- customers
-- customers 테이블을 생성한다. 상세한 schema는 첨부 파일 참고.
CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY AUTOINCREMENT, 
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT NOT NULL
);

-- customers 테이블에 서로 다른 데이터를 최소 3개 이상 삽입한다.

INSERT INTO customers (name, email, phone)
VALUES ('허균', 'hong.gildong@example.com', '010-1234-5678'), 
('김영희', 'kim.younghee@example.com', '010-9876-5432'), 
('이철수', 'lee.cheolsu@example.com', '010-5555-4444')



-- 데이터 수정
-- orders의 3번째 레코드를 삭제하시오.
DELETE FROM orders
WHERE order_id = 3;
-- customers의 1번째 레코드의 name을 '홍길동'으로 수정하시오.
UPDATE customers
SET name = '홍길동' 
WHERE customer_id = 1; 


-- 데이터 조회
-- orders와 customers의 모든 데이터를 조회하시오.

SELECT * FROM orders;
SELECT * FROM customers; 