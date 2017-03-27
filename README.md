# InForm

This repo contains the source code for the backend and the frontend.

Credits: 
* The Django-React interaction was setup by following a [great guide](http://geezhawk.github.io/using-react-with-django-rest-framework) I found on Reddit.
* The Docker-Django-Nginx-Gunicorn interaction was setup with [this](http://ruddra.com/2016/08/14/docker-django-nginx-postgres/) guide.
* The hotloader was setup with [this](http://owaislone.org/blog/webpack-plus-reactjs-and-django/) guide.
## Background knowledge

If you're not super comfortable with Python, Django, Docker, or React, check out [this](docs/learning.md) doc first.

[Here](docs/docker-commands.md) is a list of useful docker commands specific for this project.

Definitely read the [software architecture](docs/architecture.md) document too.

## Setup for development

Here are some instructions for getting the codebase up and running locally

Overview:

1. Clone the repo
2. Install docker
3. Build the docker images 
4. Run the docker containers


### Install Docker

Download and install Docker for Mac or Docker for Windows [here](https://www.docker.com/).

If you are on Windows, you may need to tell Docker that your C:\ drive is shared.

* Click on the Docker icon in your taskbar and click on settings.
* Click on Shared Drives.
* Make sure that the box for C:\ drive is checked

This is required because our docker image creates local file system volumes that our containers access (e.g. to store the sqlite database in a stateful and non-volatile environment)




### Build the docker images

Now you need to build the docker images that are defined in our docker-compose.yml file.

To do this, run the following command from the git root folder:

```bash
docker-compose build
```

### Run the docker containers

Now that you've build the images locally for our services, you need to create containers from those images to run the code.

To do this, run the following command from the git root folder:

```bash
docker-compose up -d
```

This will run our docker containers in the background on your host machine.

You can see that their status by running

```bash
docker-compose ps
```

You can bring them down with
```bash
docker-compose down
```

Check them out at localhost:8000 (you may need to give it a second to load at first)


### Done!

![](https://media.giphy.com/media/A4R8sdUG7G9TG/giphy.gif)