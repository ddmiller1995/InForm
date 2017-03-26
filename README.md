# InForm

This repo contains the source code for the backend and the frontend.

Credits: 
* The Django-React interaction was setup by following a [great guide](http://geezhawk.github.io/using-react-with-django-rest-framework) I found on Reddit.
* The Docker-Django-Nginx-Gunicorn interaction was setup with [this](http://ruddra.com/2016/08/14/docker-django-nginx-postgres/) guide.
## Background knowledge

If you're not super comfortable with Python, Django, Docker, or React, check out [this](docs/learning.md) doc first.

[Here](docs/docker-commands.md) is a list of useful docker commands specific for this project.

Definitely read the [software architecture](docs/architecture.md) document too.

## Setup for development

Here are some instructions for getting the codebase up and running locally

Overview:

1. Clone the repo
2. Install docker
4. Install node dependencies
5. Compile the JS bundle
5. Run docker
6. Collect static files
s will look something like the following (will be a different file extension on Mac, .bat is Windows only)



### Install Docker

Download and install Docker for Mac and Docker for Windows [here](https://www.docker.com/).

If you are on Windows, you may need to tell Docker that your C:\ drive is shared.

* Click on the Docker icon in your taskbar and click on settings.
* Click on Shared Drives.
* Make sure that the box for C:\ drive is checked

This is required because our docker image creates local file system volumes that our containers access (e.g. to store the sqlite database in a stateful and non-volatile environment)

### Install node dependencies

We need to download our node dependencies.

Run the following in the src directory to install the node dependencies locally (will take a while).

```bash
npm install
```

### Compile the JS bundle

The bundle js file is exluded from version control to avoid annoying meaningless merge conflicts. In other words, when you clone the repo you don't get a default empty bundle. Django will throw errors if the bundle is missing, so you need to compile it before the server is run for the first time.

**Important**:  If you make some front end code changes, this is something you will need to do frequently. You need to recompile the javascript bundle before the Django server reflects any code changes you've made. Since the bundle file is exluded from git, after you pull someone's changes down, you also need to recompile the bundle.

To compile the bundle, run the shortcut command defined in package.json from the src directory

```bash
npm run compile
```

### Compiling JS bundles

~~Now you need to compile the javascript into a bundle.~~

~~**Important**:  This is something you will need to do frequently. If you make some front end code changes, you need to recompile the javascript bundle before the Django server reflects the code changes. To prevent non-meaningful merge conflicts all the time, I've excluded the bundle files from git. This means that after you pull someone's changes down, you also need to recompile the bundle.~~

### Build the docker images

Now you need to build the docker images that are defined in our docker-compose.yml file.


To do this, run the following command from the git root folder:

```bash
docker-compose build
```

**Edit:** This command is no longer necessary, as we are now using a React Hot Loader which compiles our files on the fly and communicates any changes to our Django server. See the next section, [Running the React Hot Loader](#running-the-react-hot-loader), for more detail. 

### Running the React Hot Loader

We are now using React Hot Loader. In short, this means that we no longer have to run `npm run compile` everytime we make changes to our code. Instead, when paired with Webpack, React Hot Loader allows React components to be live reloaded without having to manually run any compile scripts or restart the server. We're also using webpack-dev-server's API to create a new instance of the server, stored as server.js, which communicates to our Django server any changes we make to our files.

You'll need to run the Django and node server simultaneously for this to work properly. Use the following npm script command to run the node server:

```bash
npm start
``` 

That's it! Though keep in mind that without using Browser-sync, or something similar, you'll still have to manually refresh the page. This just saves you from the manual recompile. 

By default, the server will keep the bundles in memory rather than writing them to disk. This is good news for us, as it means we won't end up with a new, unique bundle file everytime we make changes and compile.

[Here](http://owaislone.org/blog/webpack-plus-reactjs-and-django/) is a really great tutorial that walks through how to integrate react-hot-loader with Webpack. Read the 'Bonus: Live editing react components' section for an overview on react-hot-loader and webpack-dev-server.

**Note:** react-hot-loader and webpack-dev-loader should not be included in any production config. 

### Creating and applying database migrations

### Run the docker images


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

Check them out at localhost:8000!

You should see a blank page for now because the container doesn't have access to the bundle yet (next step)

### Collect static files

Run the following command to collect static files from within the running django container:

```bash
docker exec -it dg01 python manage.py collectstatic
```

This will run the django collectstatic command and put them in the /static folder of the django container. But since the docker file defined the /static folder to be a file system volume the same way for the django container and the nginx container, they actually share a folder with each other (and with your host machine).

This is how you can transport static files from the django container to the nginx container. This is important because nginx will be the one serving static files (not gunicorn).

### Watching your SASS files

Since we're using Sass, we also have to tell Sass to convert any changes made in our .scss files into our main.css. Open a terminal tab and run the following command:

```
sass --watch scss/base.scss:css/main.css
```

If you make style changes in our Sass files and don't see them reflected on the page, it's probably because you forgot to run this command. Remember: using Sass means that we are no longer interacting with / editing the css file directly. Only make style changes in the appropriate Sass file and let Sass communicate to main.css on its own.

### Done!

That was a lot of steps, but luckily you only have to do them when you first clone down the repo (for the most part).