FROM python:3-slim
LABEL maintainer="Raphaël HUCK <raphael.huck@gmail.com>"

ARG USER=dogmon
ARG GROUP=dogmon
ARG UID=1000
ARG GID=1000

ENV HOME="/home/${USER}"
ENV PATH="${HOME}/.local/bin:${PATH}"
  
RUN groupadd --gid $GID $GROUP && useradd -m --uid $UID --gid $GID $USER

USER ${USER}
WORKDIR /home/${USER}

COPY dist/dogmon-0.1-py3-none-any.whl .
RUN python3 -m pip install --user dogmon-0.1-py3-none-any.whl && \
    rm -f dogmon-0.1-py3-none-any.whl && \
    touch /tmp/access.log

CMD ["dogmon"]
