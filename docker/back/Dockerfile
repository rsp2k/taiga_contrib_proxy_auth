ARG TAIGA_VERSION=latest
ARG RELEASE=master
FROM taigaio/taiga-back:${TAIGA_VERSION}
RUN apt-get update && apt-get install git -y
RUN git clone https://github.com/rsp2k/taiga_contrib_proxy_auth.git && cd taiga_contrib_proxy_auth
RUN cd taiga_contrib_proxy_auth/back; pip install -e .
COPY config.py /taiga-back/settings/config.py