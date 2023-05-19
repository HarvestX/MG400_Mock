[![ci](https://github.com/HarvestX/MG400_Mock/actions/workflows/ci.yml/badge.svg)](https://github.com/HarvestX/MG400_Mock/actions/workflows/ci.yml)
[![lint](https://github.com/HarvestX/MG400_Mock/actions/workflows/lint.yml/badge.svg)](https://github.com/HarvestX/MG400_Mock/actions/workflows/lint.yml)

# MG400_Mock

Dobot MG400 Mock Server Package.
MG400_Mock let user to replace actual hardware to docker container system.
It can make more easy to develop MG400 control system with embeded IK solver.

![Image](media/system_overview.svg)

## Prerequisities

- [Docker](https://docs.docker.com/get-docker/)

## How to use

### Launch an instance

```bash
cd MG400_Mock
docker compose -f docker/docker-compose.yml up
```

If you want to launch multiple instances (e.g. 3 instances), then

```bash
docker compose -f docker/docker-compose.yml up --scale dobot=3
```

### Identify container IP address

Docker containers will run in docker's bridge network (`172.10.0.0/24`), and their IP address can be identified by the following command.

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' docker-dobot-1
```

If there are more than one docker-dobot container, their name would be `docker-dobot-2`, `docker-dobot-3` etc.

### Shutdown

```bash
docker compose -f docker/docker-compose.yml down
```

### Test (for debug)

```bash
docker compose -f docker/test-docker-compose.yml run test_dobot python3 -m unittest discover -s tests
```

## Setting user defined coordinate systems

- You can define *tool coordinate systems* through `tool.yml` in the assets folder.
- *user coordinate systems* have not been implemented yet.

## References

- [MG400_ROS2](https://github.com/HarvestX/MG400_ROS2)
- [Official ROS1 package](https://github.com/Dobot-Arm/MG400_ROS)
