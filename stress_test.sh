mysqlslap -u test -p -h localhost --create-schema=test --concurrency=10 --iterations=20 --query="SELECT * FROM elements" -P 3306
