# DualCam

Firmware code for dual camera system implemented using STM32H7A3ZITXQ board.

## Setup in STM32Cube IDE

1. Clone the repository:

        git clone https://github.com/vb000/DualCam.git
        
2. In STM32Cube IDE, create a workspace in the directory `DualCam`:

        File -> Switch Workspace -> Other -> <select path to cloned repo> -> Launch

3. Import required projects to the IDE. For eg., project `Empty_STM32H7A3ZITXQ` can be imported by:

        File -> New -> Create a New STM32 project from an Existing STM32CubeMX Configuration File (.ioc) -> .. 
        .. -> Browse -> <location of this repo>/DualCam/Empty_STM32H7A3ZITXQ/Empty_STM32H7A3ZITXQ.ioc -> Finish
        
## Adding projects/files to this repo

Ideally, we would only like to add source files and config files to this repository. Adding
generated files not only drastically increase the repo size, but also would make the code
impcompatiable on machines that's not your own.

A standard STM32 project comprises of:

```
.settings
.cproject
.project
*.ioc
Drivers/
*.ld
<C/C++/header sources>
*.launch
```

Examples of generated files are:
```
.metadata/
Debug/
```
Pattern related to generated files are added to `.gitignore` so that they would be automatically ignored by git,
when executing `git status` or `git add` commands.
