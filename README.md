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
3. Manually handle schema changes (temporary)
4. Build the docker images 
5. Run the docker containers


### Install Docker

Download and install Docker for Mac or Docker for Windows [here](https://www.docker.com/).
If you don't have Windows Professional or above, you'll need to use Docker Toolbox instead. Download [here](https://www.docker.com/products/docker-toolbox)

If you are on Windows, you may need to tell Docker that your C:\ drive is shared.

* Click on the Docker icon in your taskbar and click on settings.
* Click on Shared Drives.
* Make sure that the box for C:\ drive is checked

This is required because our docker image creates local file system volumes that our containers access (e.g. to store the sqlite database in a stateful and non-volatile environment)

### Reseting the SQLite Database

If there have been schema changes since the last time you ran the docker containers, there's a few more steps you'll need to take

First, delete all the migration files located in InForm/src/api/migrations. These are the .py files with a number in them. Next delete the db.sqlite3 file located in InForm/src

Now, if you haven't already create the virtual environment from the root repo folder using

```bash
python -m venv virtualenv
```

Run the activate program from the command line, which will look something like this:

```bash
C:\Users\luisn\Downloads\InForm> virtualenv\Scripts\activate.bat
(virtualenv) C:\Users\luisn\Downloads\InForm> 
```

Now that your virtualenv is activated, install the project's python dependencies (like Django for example) with pip:

```bash
pip install -r config/requirements.txt
```

Next you need to run database migrations, which will initialize the database with the new schema changes.

```bash
python src/manage.py makemigrations
python src/manage.py migrate
```

Now you can close out the virtual environment and continue with the rest of the docker steps. This block of instructions are only necessary because we are still making frequent schema changes, and the automatic migrations docker is doing either aren't running properly or the migrations don't go through cleanly because of the nature of the schema change. 

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

Check them out at localhost:8000 (you may need to give it a second to load at first).


If you are on docker-toolbox, you won't find the server on localhost. Run ```docker-machine ip default``` to find the IP address you need.

### Watching your SASS files

Since we're using Sass, we also have to tell Sass to convert any changes made in our .scss files into our main.css. Open a terminal tab and run the following command from within the src/assets/ directory:

```
sass --watch scss/base.scss:css/main.css
```

If you make style changes in our Sass files and don't see them reflected on the page, it's probably because you forgot to run this command. Remember: using Sass means that we are no longer interacting with / editing the css file directly. Only make style changes in the appropriate Sass file and let Sass communicate to main.css on its own.

### Done!

![](https://media.giphy.com/media/A4R8sdUG7G9TG/giphy.gif)
