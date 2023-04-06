# Introduction
This project is London Market's Cloud Data Platform

# Getting started for developers
The build for the Cloud Data Platform runs on Python within a Docker container held on Hiscox Artifactory. The same container is used for development.
## Environment
This is a Docker build supported on Windows Subsystem for Linux on a Citrix desktop only, as this ensures the required network connectivity.

### Note on line endings
As this is a unix environment we use `lf` line endings rather than the Windows standard `crlf`. Git for Windows can be configured to not convert these using the below command.
```
git config --global core.autocrlf input
```

## Prerequisites
1. Get an HGD10+ machine with [HyperV](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v) enabled in both the operating system and BIOS. This must be done my IT Services when provisioning the machine.
2. Enable [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
3. Install the prebuilt [WSL Ubuntu distribution](https://hiscox.atlassian.net/wiki/spaces/LTT/pages/3456959475/DAT-ENG+-+Run+docker+using+Ubuntu+WSL2+within+Citrix#Using-the-prebuilt-WSL-Ubuntu-20.04-distribution-(docker-already-installed)) for this project.
4. Check out the [`LM-DataStrategy-Config-ExposureManagement`](https://hiscoxinsurance.visualstudio.com/LM-DataStrategy/_git/LM-DataStrategy-Config-ExposureManagement) repository in the same directory as this repository.

## Setup steps
1. Generate an API key for Artifactory.
Navigate to your [profile](https://artifactory.hiscox.com/artifactory/webapp/#/profile) and login with SSO. More detailed instruction are available on the [LM Tech Confluence](https://hiscox.atlassian.net/wiki/spaces/LTT/pages/1655376132/Artifactory#How-to-Configure-your-user-API-Key-for-use-in-Artifactory).


2. Set low level environment variables in Windows.
   * CDP__ARTIFACTORY__USERNAME - Set to your Hiscox email address `your.name@hiscox.com`
   * CDP__ARTIFACTORY__PASSWORD - Use the API key generated in Step 1.
   * CDP__SETTINGS_FILE - The settings file you want to use for local builds. Typically `python/cdpsettings/settings-local.json`
   * HTTP_PROXY - `zsproxy2.hiscox.com:80`

3. [Map](https://devblogs.microsoft.com/commandline/share-environment-vars-between-wsl-and-windows/) Windows environment variables to WSL environment variables by setting the `WSLENV` Windows environment variable to.
```
CDP__SETTINGS_FILE:CDP__SETTINGS_FILE:HTTP_PROXY:HTTP_PROXY:CDP__ARTIFACTORY__USERNAME:CDP__ARTIFACTORY__USERNAME:CDP__ARTIFACTORY__PASSWORD:CDP__ARTIFACTORY__PASSWORD:
```

4. Start the WSL distribution. All other commands should be run within that distribution.
```
wsl -d UbuntuDocker10Plus
```

5. Login to Artifactory to download Python packages.
```
docker login -u $CDP__ARTIFACTORY__USERNAME -p $CDP__ARTIFACTORY__PASSWORD lm-devops-docker.artifactory.hiscox.com
```

6.	Login to ACR to download and publish Docker images. The login details can be found in KeePass under `Azure Container Registry > New ACR devtestacrnortheurope`
```
docker login http://devtestacrnortheurope.azurecr.io
```

7. Create  the settings file defined in the previous step e.g `python/cdpsettings/settings-local.json`. The template settings file [`python/cdpsettings/settings-citrix.json`](https://hiscoxinsurance.visualstudio.com/LM-DataStrategy/_git/LM-DataStrategy?path=/python/cdpsettings/settings-citrix.json) can serve as a template. A sample verion of this file with shared secrets can be found in the project [Keepass](https://hiscox.sharepoint.com/:u:/r/sites/LMSquads/Shared%20Documents/Data%20Strategy/CDP.kdbx?csf=1&web=1&e=AJH9sI). There are some personal secrets that must be set individually. These are described in the [settings schema](https://hiscoxinsurance.visualstudio.com/LM-DataStrategy/_git/LM-DataStrategy?path=/test/unit/python/cdpsettings/settings_schema.json). Environment prefixes should be uppercase letters.
For local development, please set `terraform` and `docker` to `false`
There are [some](https://hiscox.atlassian.net/browse/LMDSI-1386) [tickets](https://hiscox.atlassian.net/browse/LMDSI-1261) to enable terraform and docker for local development

8. Run the build in the Docker container
```
./build.sh
```

## Interactive mode
It is useful to be able to run the build container interactively during the development process. This can be done using the following command.
```
./interactive.sh
```
To run the full build locally run the following command (this will use the default LOCAL_BUILD) behaviour.
```
python3 -m cdppipeline.cli lm_data_strategy
```
The Python build can also be run as a module by defining the sequence to run. The example below runs the PRE_BUILD sequence.
```
python3 -m cdppipeline.cli lm_data_strategy --build-sequence PRE_BUILD
```
### Unit testing
To run an individual unit test file you can run the following command substituting the path to the file you want to run.
```
pytest -vs test/unit/python/path/to/unit/test
```

## Local Prefect agent container
1. Log in to the Azure Container Registry that hosts the image.
```
docker login devtestacrnortheurope.azurecr.io
```
2. Configure the runner token used to connect to Prefect cloud and the environment_prefix either in the environmet file `docker\prefect\agent\local.env file` or using system environment variables.
3. Use Docker compose to bring the agent up and run in the background.
```
./agent.sh
```
The folder `python\cdpprefect` is mounted to the agent and local changes will update the running agent.

## Cleaning up Docker images
Sometimes issues can be caused by running old versions of our containers. For example Python errors in the build can occur with an old container version. To clean up the local cache of Docker images run the following command.
```
docker system prune -a
```

## Problem with Character Length String

1. When checking out a branch you may get an error "Git cannot start.... Filename too long"
This error can be fixed by reviewing the following page:
https://stackoverflow.com/questions/22575662/filename-too-long-in-git-for-windows
https://www.youtube.com/watch?v=lJKKSoEHk5A


