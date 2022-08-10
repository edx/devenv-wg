FROM docker.io/ubuntu:20.04

RUN apt update && \
  apt install -y curl git-core language-pack-en libmysqlclient-dev libssl-dev python3 python3-pip python3-venv

ARG APP_USER_ID=1000
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

# Create python venv
RUN python3 -m venv /openedx/venv/
ENV PATH "/openedx/venv/bin:$PATH"
RUN pip install setuptools==62.1.0 pip==22.0.4 wheel==0.37.1

# Install edx-exams
ARG EXAMS_REPOSITORY=https://github.com/edx/edx-exams.git
ARG EXAMS_VERSION=main
RUN mkdir -p /openedx/exams && \
    git clone $EXAMS_REPOSITORY --branch $EXAMS_VERSION --depth 1 /openedx/exams
WORKDIR /openedx/exams

# Identify tutor user to cherry-pick commits
RUN git config --global user.email "tutor@overhang.io" \
  && git config --global user.name "Tutor"

# python requirements
RUN pip install -r requirements.txt

# Install uwsgi
# https://pypi.org/project/uWSGI/
RUN pip install uwsgi==2.0.20 django-redis==5.2.0

# Collect static assets (aka: "make static")
COPY --chown=app:app assets.py ./edx_exams/settings/assets.py
RUN DJANGO_SETTINGS_MODULE=edx_exams.settings.assets make static

# TODO: Figure out why this isn't executable
# I don't think this should be here
RUN chmod +x manage.py

# TODO: This should be production and then overriden by the dev
# compose files
ENV DJANGO_SETTINGS_MODULE edx_exams.settings.tutor.development

# Run server
EXPOSE 8740
CMD uwsgi \
    --static-map /static=/openedx/exams/edx_exams/assets \
    --static-map /media=/openedx/exams/edx_exams/media \
    --http 0.0.0.0:8740 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=2 \
    --buffer-size=8192 \
    --wsgi-file ecommerce/wsgi.py