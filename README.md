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
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Launch
```bash
git clone git@github.com:HarvestX/MG400_Mock.git
cd MG400_Mock
make
```

## Shutdown
```bash
make down
```

## Connecting with MG400_ROS2
[See](https://github.com/HarvestX/MG400_ROS2/tree/main/mg400_bringup#connect-launch-server-with-mg400_mock)

## Develop
### Running test
```bash
make test
```


## References
- [MG400_ROS2](https://github.com/HarvestX/MG400_ROS2)
- [Official ROS1 package](https://github.com/Dobot-Arm/MG400_ROS)

