ifndef CIRCLE_BRANCH
override CIRCLE_BRANCH = $(shell git rev-parse --abbrev-ref HEAD)
endif

ifndef CIRCLE_TAG
override CIRCLE_TAG = latest
endif



all: clean test build

build: build-front build-back

build-front:
	cd front && npm install && npm run build
	echo $(CIRCLE_BRANCH)
	docker build --no-cache docker/front -t akshayfpl/fpltiaga:taiga-front-openid  --build-arg RELEASE=$(CIRCLE_BRANCH) --build-arg TAIGA_VERSION=$(CIRCLE_TAG)
	
build-back:
	docker build --no-cache docker/back -t akshayfpl/fpltiaga:taiga-back-openid  --build-arg RELEASE=$(CIRCLE_BRANCH) --build-arg TAIGA_VERSION=$(CIRCLE_TAG)

publish:
	docker push fpltiaga/taiga-back-openid:$(CIRCLE_TAG)
	docker push fpltiaga/taiga-front-openid:$(CIRCLE_TAG)


