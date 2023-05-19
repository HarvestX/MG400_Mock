[![ci](https://github.com/HarvestX/MG400_Mock/actions/workflows/ci.yml/badge.svg)](https://github.com/HarvestX/MG400_Mock/actions/workflows/ci.yml)
[![lint](https://github.com/HarvestX/MG400_Mock/actions/workflows/lint.yml/badge.svg)](https://github.com/HarvestX/MG400_Mock/actions/workflows/lint.yml)

# MG400_Mock

Dobot MG400 Mock Server Package.
MG400_Mock let user to replace actual hardware to docker container system.
It can make more easy to develop MG400 control system with embeded IK solver.

![Image](media/mg400_mock.gif)

![Image](media/system_overview.svg)

## Requirements

- [Docker](https://docs.docker.com/get-docker/)

---

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
