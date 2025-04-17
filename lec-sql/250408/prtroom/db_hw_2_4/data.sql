-- check
SELECT * FROM orders;

-- orders 테이블을 삭제한다.
DROP TABLE orders; 
-- orders 테이블을 첨부 파일을 참고하여 다시 생성한다. customer와 관계를 형성한다.

CREATE TABLE orders(
  order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
  order_date DATE NOT NULL, 
  total_amount REAL NOT NULL, 
  customer_id INTEGER NOT NULL
);


-- 각 주문 당 주문자가 누구인지 확인할 수 있으면 정말 좋겠다 
-- 그리고 그 방법은 외부 키를 이용하면 될 거 같다
-- 그니까 orders에서 customers_id 컬럼을 만들 건데 (fk로 사용됨)
-- 이 아이디는 customers에서 사람들의 pk값이면 되겠지 
SELECT * FROM orders
INNER JOIN customers
 ON orders.customer_id = customers.customer_id; 




-- 쿼리문을 사용하여 orders 테이블을 수정한다 

-- orders 테이블에 Integer 타입의 price 컬럼 추가한다. 
ALTER TABLE orders
ADD COLUMN 
price INTEGER NOT NULL DEFAULT 'default value';

-- orders 테이블의 total_amount 컬럼을 삭제한다.
ALTER TABLE orders 
DROP COLUMN total_amount; 

-- orders 테이블에 데이터를 최소 3개 이상 생성한다. 
INSERT INTO orders (order_date, customer_id, price)
-- INSERT INTO orders 
VALUES 
('2023-07-15', 1, 50), 
('2023-07-16', 2, 75), 
('2023-07-17', 3, 30);

-- (1, '2023-07-15', 1, 50), 
-- (2, '2023-07-16', 2, 75), 
-- (3, '2023-07-17', 3, 30);


-- Date 타입은 'YYYY-MM-DD' 형식으로 삽입한다. 
-- Real 타입은 10.11 형식으로 삽입한다. 
-- 데이터를 생성할 때 customers_id도 함께 삽입한다.

-- orders의 모든 데이터를 조회한다. 단, 관계를 맺고 있는 customers의 name도 함께 출력한다.


-- SELECT * FROM orders;
-- SELECT * FROM orders;

SELECT orders.order_id, customers.name, orders.order_date, orders.price FROM orders
INNER JOIN customers
  ON customers.customer_id = orders.customer_id;