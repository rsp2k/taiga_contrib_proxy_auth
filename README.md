taiga-contrib-proxy-auth
=========================
A Proxy Authentication Plugin
- Uses headers from reverse proxy to authenticate users
Based on: [taiga-contrib-github-auth](https://github.com/taigaio/taiga-contrib-github-auth).

Compatible with Taiga 4.2.1, 5.x, 6

# Installation

## Docker
This plugin is compatible with the offical taiga docker images 😃

https://github.com/taigaio/taiga-docker

This project builds 2 images based off the images provided by taiga. This should allow other customisations to continue to work.

The following will show the changes needed to the default docker-compose file to install the openid plugin.

### Config 
The 2 images:
 - taiga-front-proxy-auth
 - taiga-back-proxy-auth

Use the following environmental setting to configure the frontend conf.json and backed settings.py

```
ENABLE_OPENID: "True"

```

The following are optional fields to configure the mapping between keycloak and taiga if left blank the defaults will be used
```
OPENID_ID_FIELD = "sub"
```


### Docker-compose file modified from https://github.com/taigaio/taiga-docker
```
version: "3.5"

x-environment:
  &default-back-environment
  # Database settings
  POSTGRES_DB: taiga
  POSTGRES_USER: taiga
  POSTGRES_PASSWORD: taiga
  POSTGRES_HOST: taiga-db
  # Taiga settings
  TAIGA_SECRET_KEY: "taiga-back-secret-key"
  TAIGA_SITES_DOMAIN: "localhost:9000"
  TAIGA_SITES_SCHEME: "http"
  # Email settings. Uncomment following lines and configure your SMTP server
  # EMAIL_BACKEND: "django.core.mail.backends.smtp.EmailBackend"
  # DEFAULT_FROM_EMAIL: "no-reply@example.com"
  # EMAIL_USE_TLS: "False"
  # EMAIL_USE_SSL: "False"
  # EMAIL_HOST: "smtp.host.example.com"
  # EMAIL_PORT: 587
  # EMAIL_HOST_USER: "user"
  # EMAIL_HOST_PASSWORD: "password"
  # Rabbitmq settings
  # Should be the same as in taiga-async-rabbitmq and taiga-events-rabbitmq
  RABBITMQ_USER: taiga
  RABBITMQ_PASS: taiga
  # RabbitMQ Fixes
  CELERY_BROKER_URL: "amqp://taiga:taiga@taiga-async-rabbitmq:5672/taiga"
  EVENTS_PUSH_BACKEND: "taiga.events.backends.rabbitmq.EventsPushBackend"
  EVENTS_PUSH_BACKEND_URL: "amqp://taiga:taiga@taiga-events-rabbitmq:5672/taiga"
                

  
  # Telemetry settings
  ENABLE_TELEMETRY: "True"
  
  # Enable OpenID to allow to register users if they do not exist. Set to false to disable all signups
  PUBLIC_REGISTER_ENABLED: "True"

  # OpenID settings
  ENABLE_OPENID: "True"
  OPENID_USER_URL : "https://{url-to-keycloak}/auth/realms/{realm}/protocol/openid-connect/userinfo"
  OPENID_TOKEN_URL : "https://{url-to-keycloak}/auth/realms/{realm}/protocol/openid-connect/token"
  OPENID_CLIENT_ID : "<CLient ID>"
  OPENID_CLIENT_SECRET : "<CLient SECRET>"
  OPENID_SCOPE="openid email"

x-volumes:
  &default-back-volumes
  - taiga-static-data:/taiga-back/static
  - taiga-media-data:/taiga-back/media
  # - ./config.py:/taiga-back/settings/config.py


services:
  taiga-db:
    image: postgres:12.3
    environment:
      POSTGRES_DB: taiga
      POSTGRES_USER: taiga
      POSTGRES_PASSWORD: taiga
    volumes:
      - taiga-db-data:/var/lib/postgresql/data
    networks:
      - taiga

  taiga-back:
    image: robrotheram/taiga-back-proxy-auth
    environment: *default-back-environment
    volumes: *default-back-volumes
    networks:
      - taiga
    depends_on:
      - taiga-db
      - taiga-events-rabbitmq
      - taiga-async-rabbitmq

  taiga-async:
    image: taigaio/taiga-back:latest
    entrypoint: ["/taiga-back/docker/async_entrypoint.sh"]
    environment: *default-back-environment
    volumes: *default-back-volumes
    networks:
      - taiga
    depends_on:
      - taiga-db
      - taiga-back
      - taiga-async-rabbitmq

  taiga-async-rabbitmq:
    image: rabbitmq:3-management-alpine
    environment:
      RABBITMQ_ERLANG_COOKIE: secret-erlang-cookie
      RABBITMQ_DEFAULT_USER: taiga
      RABBITMQ_DEFAULT_PASS: taiga
      RABBITMQ_DEFAULT_VHOST: taiga
    volumes:
      - taiga-async-rabbitmq-data:/var/lib/rabbitmq
    networks:
      - taiga

  taiga-front:
    image: robrotheram/taiga-front-proxy-auth
    environment:
      TAIGA_URL: "http://localhost:9000"
      TAIGA_WEBSOCKETS_URL: "ws://localhost:9000"
      ENABLE_OPENID: "true"
    networks:
      - taiga
    # volumes:
    #   - ./conf.json:/usr/share/nginx/html/conf.json

  taiga-events:
    image: taigaio/taiga-events:latest
    environment:
      RABBITMQ_USER: taiga
      RABBITMQ_PASS: taiga
      TAIGA_SECRET_KEY: "taiga-back-secret-key"
    networks:
      - taiga
    depends_on:
      - taiga-events-rabbitmq

  taiga-events-rabbitmq:
    image: rabbitmq:3-management-alpine
    environment:
      RABBITMQ_ERLANG_COOKIE: secret-erlang-cookie
      RABBITMQ_DEFAULT_USER: taiga
      RABBITMQ_DEFAULT_PASS: taiga
      RABBITMQ_DEFAULT_VHOST: taiga
    volumes:
      - taiga-events-rabbitmq-data:/var/lib/rabbitmq
    networks:
      - taiga

  taiga-protected:
    image: taigaio/taiga-protected:latest
    environment:
      MAX_AGE: 360
      SECRET_KEY: "taiga-back-secret-key"
    networks:
      - taiga

  taiga-gateway:
    image: nginx:1.19-alpine
    ports:
      - "9000:80"
    volumes:
      - ./taiga-gateway/taiga.conf:/etc/nginx/conf.d/default.conf
      - taiga-static-data:/taiga/static
      - taiga-media-data:/taiga/media
    networks:
      - taiga
    depends_on:
      - taiga-front
      - taiga-back
      - taiga-events

volumes:
  taiga-static-data:
  taiga-media-data:
  taiga-db-data:
  taiga-async-rabbitmq-data:
  taiga-events-rabbitmq-data:

networks:
  taiga:
```

### Docker building

For Docker building for new release make sure that the following files are coppied into the docker directory

**Backend:**
Copy https://raw.githubusercontent.com/taigaio/taiga-back/master/docker/config.py

**Frontend:**
copy the config.json and config_env_subst.sh from https://github.com/taigaio/taiga-front/tree/master/docker



## Manual installation
### Taiga Backend

Clone the repo and
```bash
cd taiga-contrib-proxy-auth/back
workon taiga
pip install -e .
```

Modify `taiga-back/settings/local.py` and include the line:

```python
INSTALLED_APPS += ["taiga_contrib_proxy_auth"]
OPENID_USER_URL = "https://{url-to-keycloak}/auth/realms/{realm}/protocol/openid-connect/userinfo"

```

## Taiga Frontend

Clone the repo and then link `dist` to the `taiga-front` plugins directory:

```bash
mkdir {path-to-taiga-frontend}/plugins
ln -s {path-to-taiga-contrib-proxy-auth}/dist {path-to-taiga-frontend}/plugins/proxy-auth
```

Add the following values to `{path-to-taiga-frontend}/conf.json`:

```json
{
  "openidAuth" : "https://{url-to-keycloak}/auth/realms/{realm}/protocol/openid-connect/auth",
  "contribPlugins": [
      "/plugins/proxy-auth/proxy-auth.json"
  ]
}
```

# Building

The make file contains the basic blocks to locally build the UI and docker containers.

```
make build
```


