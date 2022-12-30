### STAGE 1 ###
FROM node:19-alpine AS frontend
ARG PROJECT={{cookiecutter.project_slug}}
WORKDIR /code

ADD assets/package.json assets/yarn.lock assets/
RUN cd assets && yarn install
ADD assets/ assets/
ADD $PROJECT $PROJECT

RUN cd assets && yarn build
VOLUME /code/

### STAGE 2 ###

FROM python:{{cookiecutter.python_version}}-slim
ARG REPO_URL=''
LABEL org.opencontainers.image.source $REPO_URL
ARG PROJECT={{cookiecutter.project_slug}}

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1
EXPOSE 8000
WORKDIR /code

RUN set -xe \
    && RUN_DEPS="gettext nano procps" \
    && apt update -y \
    && apt install -y --no-install-recommends $RUN_DEPS \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

ADD pyproject.toml poetry.lock ./
RUN set -xe \
    && BUILD_DEPS="git" \
    && apt update -y \
    && apt install -y --no-install-recommends $BUILD_DEPS \
    && update-ca-certificates \
    && pip install poetry --no-cache-dir \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --without dev --no-root --no-cache \
    && pip uninstall -y poetry \
    && pip cache purge || true \
    && rm -rf ~/.cache/pypoetry/{cache,artifacts} \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

ADD $PROJECT/ $PROJECT/
ADD alembic/ alembic/
ADD alembic.ini pybabel.ini ./
ADD manage.py ./

COPY --from=frontend /code/$PROJECT/statics/ $PROJECT/statics/
RUN groupadd -r app && useradd -r -m -g app app

ARG RELEASE_ID=''
ENV RELEASE_ID=$RELEASE_ID

ARG CI_COMMIT_REF_SLUG=''
ENV CI_COMMIT_REF_SLUG=$CI_COMMIT_REF_SLUG

ARG CI_COMMIT_SHA=''
ENV CI_COMMIT_SHA=$CI_COMMIT_SHA

ARG CI_BUILD_DATE=''
ENV CI_BUILD_DATE=$CI_BUILD_DATE

RUN pybabel compile -d $PROJECT/locales/
RUN echo "Commit Ref = ${CI_COMMIT_REF_SLUG} - Commit SHA = ${CI_COMMIT_SHA} - Built at = " ${CI_BUILD_DATE} > ./version
SHELL ["/bin/bash"]

ADD scripts/* /bin/
CMD ["/bin/docker-run.sh"]
