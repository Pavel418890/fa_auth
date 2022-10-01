FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /home/app/src/

RUN addgroup --system --gid 1000 app && \
    adduser --system --gid 1000 --uid 1000 app

COPY . .

ARG INSTALL_DEV=true

#RUN addgroup --system --gid 1000 app && \
#    adduser --system --gid 1000 --uid 1000 app && \
RUN \
    chown -R 1000:1000 . && chmod +x ./scripts/*.sh && \
    if [ $INSTALL_DEV == true ] ; then \
    pip install \
    --no-cache-dir \
    --no-deps \
    -r requirements.dev.txt ; else \
    pip install \
    --no-cache-dir \
    --no-deps \
    -r requirements.txt ; \
    fi
ENV PYTHONPATH $HOME/src

USER app