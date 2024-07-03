taiga-contrib-proxy-auth
=========================
A Proxy Authentication Plugin
- Uses headers from reverse proxy to authenticate users
Based on: [taiga-contrib-github-auth](https://github.com/taigaio/taiga-contrib-github-auth).

Compatible with Taiga 4.2.1, 5.x, 6

# Installation

## Docker
This plugin is compatible with the official taiga docker images 😃

https://github.com/taigaio/taiga-docker

This project builds 1 image based off the image provided by taiga. This should allow other customisations to continue to work.

The following will show the changes needed to the default docker-compose file to install the proxy auth plugin.

### Config 
The 1 image:
 - taiga-back-proxy-auth

Set the following in backed settings.py (defaults shown):
```
PROXY_USERNAME_FIELD = "X-PROXY-USER"
PROXY_FULLNAME_FIELD = "X-PROXY-NAME"
PROXY_EMAIL_FIELD = "X-PROXY-EMAIL"
```


Add these environment variables to the x-environment: section in your docker-compose.yml
```yaml
  PROXY_USERNAME_FIELD: "X-PROXY-USER"
  PROXY_FULLNAME_FIELD: "X-PROXY-NAME"
  PROXY_EMAIL_FIELD: "X-PROXY-EMAIL"
```

Change the `image:` section in the `taiga-back` service
```
    image: rsp2k/taiga-back-proxy-auth
```

### Docker building

For Docker building for new release make sure that the following files are coppied into the docker directory

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
```

# Building

The make file contains the basic blocks to locally build the docker container.

```
# Build it
make build

# Publish to docker hub. NB: Change image= to point to your docker hub repo
make image=rsp2k/taiga-back-proxy-auth publish
```