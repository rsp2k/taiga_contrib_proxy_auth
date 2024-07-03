ifndef CIRCLE_BRANCH
override CIRCLE_BRANCH = $(shell git rev-parse --abbrev-ref HEAD)
endif

ifndef CIRCLE_TAG
override CIRCLE_TAG = latest
endif



all: clean test build

build: build-back

build-back:
	docker build --no-cache docker/back -t rsp2k/taiga-back-proxy-auth  --build-arg RELEASE=$(CIRCLE_BRANCH) --build-arg TAIGA_VERSION=$(CIRCLE_TAG)

publish:
    docker push rsp2k/taiga-back-proxy-auth:$(CIRCLE_TAG)


