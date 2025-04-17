-- 공통
SELECT * FROM articles;
DROP TABLE articles;
PRAGMA table_info('articles');

CREATE TABLE articles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title VARCHAR(100) NOT NULL,
  content VARCHAR(200) NOT NULL,
  createdAt DATE NOT NULL
);


-- 1. Insert data into table

INSERT INTO articles (title, content, createdAt)
VALUES ('hello', 'world', '2000-01-01');

-- 컬럼에 값 채워넣는거 동작 되는지 안되는지 어떻게하면 동시가능인지 
-- 방법1 -- 됨됨
INSERT INTO articles (title, content, createdAt)
VALUES 
('title1', 'content1', '1900-01-01'),
('title2', 'content2', '1800-01-01'),
('title3', 'content3', '1700-01-01')

-- 방법2 -- 안됨
INSERT INTO articles (title, content, createdAt)
VALUES 
('title1', 'content1', '1900-01-01'),
VALUES 
('title2', 'content2', '1800-01-01'),
VALUES 
('title3', 'content3', '1700-01-01')



INSERT INTO articles (title, content, "createdAt")
VALUES ('mytitle', 'mycontent', DATE());




-- 2. Update data in table
SELECT * FROM articles;



UPDATE 
  articles
SET 
  title = 'update Title', 
  content = 'update Content'
WHERE
  id = 2;


-- 3. Delete data from table

DELETE FROM 
  articles
WHERE 
  id = 7;

-- 올 ㅋ 아이디 중간에 있는 거 삭제하면 id값이 떙겨지거나 하진 않네 



-- 심화

DELETE FROM articles
-- WHERE id = ??? id 조회를 해주고 싶은데 모르니깐!! 작성한 지 오래된 게시글 2개

SELECT id
FROM articles
ORDER BY "createdAt";


SELECT *
FROM articles


DELETE FROM 
  articles
WHERE id IN (
  SELECT id 
  FROM articles
  ORDER BY "createdAt"
  LIMIT 2 
);
