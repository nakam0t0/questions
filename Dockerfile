FROM python:3.6

MAINTAINER Shogo Nakamoto

ADD . /flask/

WORKDIR /flask/

RUN apt-get update \
    && apt-get install -y zsh \
    curl \
    wget \
    git \
    vim \
    && sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" \
    && pip install -r requirements.txt \
    && touch manage.py \
    && mkdir -p app/{static,templates} \
    && touch app/{__init__,views,models,config}.py \
    && touch app/static/style.css \
    && touch app/templates/{layout,show,login,admin}.html \
