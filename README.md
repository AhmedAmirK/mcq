# MCQ Test and Scoring apps
2 django microservices, 2 mysql databases, zookeeper and kafka for messaging queue
## To run the app:
1) docker-compose up -d
2) docker exec -it mcq-mcq_test-1 /bin/sh
3) python manage.py makemigrations
4) python manage.py migrate
5) docker exec -it mcq-mcq_scoring-1 /bin/sh
6) python manage.py makemigrations
7) python manage.py migrate
8) API ready to use
