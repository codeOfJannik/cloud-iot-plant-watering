For this project the GitLab CI-Runner is used and was installed with the help of the [installation 
documentation](https://docs.gitlab.com/runner/install/linux-manually.html) and [configuration 
documentation](https://docs.gitlab.com/runner/configuration/advanced-configuration.html). The runner is set up on a AWS
EC2 instance. See [.gitlab-ci.yml](.gitlab-ci.yml) for details about the ci-runner usage.

Docker Image, which is used by the CI-Runner (located add ./Dockerfile):

```python
FROM alpine:latest

RUN apk update
RUN apk add --update-cache python3 py-pip
RUN pip3 install pip AWSIoTPythonSDK
RUN pip3 install pip pyyaml
```
This Dockerfile must be built with _"sudo docker build --no-cache -t chronos/ci-image ."_

The GitLab CI-Runner config.toml (located at /etc/gitlab-runner/config.toml):

```python
concurrent = 10
check_interval = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "ci-runner chronos"
  url = "https://gitlab.mi.hdm-stuttgart.de/"
  token = "svhs_ZYsEE5TQ6_xHmqs"
  executor = "docker"
  [runners.custom_build_dir]
  [runners.cache]
  [runners.docker]
    tls_verify = false
    image = "chronos/ci-image:latest" # build local image is required 
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 0
   pull_policy = "if-not-present"
```