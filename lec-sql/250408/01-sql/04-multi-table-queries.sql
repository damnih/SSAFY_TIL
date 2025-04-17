-- 공통
SELECT * FROM articles;
SELECT * FROM users;
DROP TABLE articles;
DROP TABLE users;
PRAGMA table_info('articles');


-- 실습용 데이터
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(50) NOT NULL
);

CREATE TABLE articles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title VARCHAR(50) NOT NULL,
  content VARCHAR(100) NOT NULL,
  userId INTEGER NOT NULL,
  FOREIGN KEY (userId) 
    REFERENCES users(id)
);

INSERT INTO 
  users (name)
VALUES 
  ('하석주'),
  ('송윤미'),
  ('유하선');

INSERT INTO
  articles (title, content, userId)
VALUES 
  ('제목1', '내용1', 1),
  ('제목2', '내용2', 2),
  ('제목3', '내용3', 1),
  ('제목4', '내용4', 4),
  ('제목5', '내용5', 1);


-- INNER JOIN
-- 1단계. 두 테이블 결합 후 조건에 만족하는 모든 필드 조호 ㅣ
-- 작성자가 존재하는 모든 게시물을 출력 

SELECT * FROM articles
INNER JOIN users 
  ON users.id = articles.userId; 

-- 2단계. 최종 출력 필드에 맞게 타이틀과 네임만 셀렉트 
SELECT title, name FROM articles
INNER JOIN users 
  ON users.id = articles.userId; 

-- 3단계. 1번 작성자가 작성한 게시물만 조회 
SELECT articles.title, users.name FROM articles
INNER JOIN users 
  ON users.id = articles.userId;
WHERE 
  users.id = 1;


-- LEFT JOIN


-- 
SELECT * FROM users
LEFT JOIN articles
ON articles.userId = users.id


-- 2단계. 1단계 결과에서 결국 article 정보가 NULL 사용자가 게시글을 작성성

SELECT * FROM users
LEFT JOIN articles
ON articles.userId = users.id
WHERE articles.userId IS NULL; 


-- 3단계. 2단계 출력에서 문제 요구사항에 맞게 사용자 이름만 출력 
SELECT users.name FROM users
LEFT JOIN articles
ON articles.userId = users.id
WHERE articles.userId IS NULL; 