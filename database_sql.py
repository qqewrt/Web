# DB 생성
# CREATE DATABASE gangnam CHARACTER SET utf8 COLLATE utf8_general_ci;

# topic table 생성
# CREATE TABLE `topic` (
# 	`id` int(11) NOT NULL AUTO_INCREMENT,
# 	`title` varchar(100) NOT NULL,
# 	`description` text NOT NULL,
# 	`author` varchar(30) NOT NULL,
# 	PRIMARY KEY (id)
# 	) ENGINE=innoDB DEFAULT CHARSET=utf8;

import pymysql

db = pymysql.connect(
    host='localhost', 
    user='root', 
    password='1234', 
    db='gangnam', 
    charset='utf8mb4')

cur = db.cursor()


# 조회

# query = 'SELECT * FROM topic'

# cur.execute(query)

# db.commit()

# data = cur.fetchall()

# print(data)


#삽입

# query = 'INSERT INTO `gangnam`.`topic` (`id`, `title`, `description`, `author`)\
#     VALUES (2 ,"자바" ,"자바(영어: Java)는 썬 마이크로시스템즈의 제임스 고슬링(James Gosling)과 다른 연구원들이 개발한 객체 지향적 프로그래밍 언어이다.\
#     1991년 그린 프로젝트(Green Project)라는 이름으로 시작해 1995년에 발표했다.\
#     처음에는 가전제품 내에 탑재해 동작하는 프로그램을 위해 개발했지만 현재 웹 애플리케이션 개발에 가장 많이 사용하는 언어 가운데 하나이고, \
#     모바일 기기용 소프트웨어 개발에도 널리 사용하고 있다. 현재 버전 15까지 출시했다.", "GARY");'

# cur.execute(query)

# db.commit()

# db.close()


#수정

# query = "UPDATE `topic` SET `title` = 'JAVA' WHERE (`id` = '2');"

# cur.execute(query)

# db.commit()

# db.close()


#삭제

# query = "DELETE FROM `gangnam`.`topic` WHERE (`id` = '2');"

# cur.execute(query)

# db.commit()

# db.close()

query = ''' 
        CREATE TABLE users(
            id INT(11) AUTO_INCREMENT PRIMARY KEY, 
            name VARCHAR(100),
            email VARCHAR(100),
            username VARCHAR(30),
            password VARCHAR(100),
            register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
    '''

cur.execute(query)

db.commit()

db.close()

