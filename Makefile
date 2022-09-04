
default: init up

init:
	docker-compose -f docker/docker-compose.yml build

up:
	docker-compose -f docker/docker-compose.yml up

down:
	docker-compose -f docker/docker-compose.yml down

test:
	docker-compose -f docker/test-docker-compose.yml run test_dobot python3 -m unittest discover -s tests
