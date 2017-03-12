# InForm

This repo contains the source code for the backend and the frontend.

## Background knowledge

If you're not super comfortable with Python, Django, or React, check out [this](docs/learning.md) doc first.

Definitely read the [software architecture](doc/architecture.md) document too.

## Python3

For simplicity's sake, let's all use the same Python version. Let's go with the latest Python 3.6. Probably any Python3 version will work, but if you haven't installed Python yet, use [Python3.6](https://www.python.org/downloads/release/python-360/) so we are all on the same page.

## Setup for development

Here are some instructions for getting the codebase up and running locally

Overview:

1. Clone the repo
2. Create a python virtual environment
3. Activate the virtual environment
3. Install the pip dependencies
4. Install node dependencies
5. Compile the JS bundle
5. Run database migrations
6. Run the dev server

### Python virtual environments

To create the virtual environment, first cd into the root repo folder then run:

```bash
python -m venv virtualenv
```

This will create a python virtual environment in the project folder. This will make it so that python dependencies get installed locally in that virtual environment, instead of the global environment. That way your dependencies for this project won't collide with any other python modules you may have previously installed.

To activate the virtual environment, run the activate program from the command line inside the virtualenv's Scripts folder. This will look something like the following (will be a different file extension on Mac, .bat is Windows only)

```bash
C:\Users\luisn\Downloads\InForm> virtualenv\Scripts\activate.bat
(virtualenv) C:\Users\luisn\Downloads\InForm> 
```
**Note**: You will need to activate your virtualenv everytime you open a new terminal and want to run the server from it.

### Installing Python dependencies

Now that your virtualenv is activated, install the project's python dependencies (like Django for example) with pip:

```bash
pip install -r requirements.txt
```

For people with a node background, requirements.txt is analogous to package.json, and pip is analogous to npm.

### Installing Node dependencies

Speaking of npm, now that the backend dependencies are installed, we need to install the frontend dependencies. Run the following to install the node dependencies locally (will take a while)

```bash
npm install
```

### Compiling JS bundles

Now you need to compile the javascript into a bundle.

**Important**:  This is something you will need to do frequently. If you make some front end code changes, you need to recompile the javascript bundle before the Django server reflects the code changes. To prevent non-meaningful merge conflicts all the time, I've excluded the bundle files from git. This means that after you pull someone's changes down, you also need to recompile the bundle.

To compile the bundle, use the shortcut command defined in package.json

```bash
npm run compile
```

### Creating and applying database migrations

Now you need to make the database migrations, and then apply them.

You are probably thinking: what the fuck are database migrations?

Remember in Info 340 that you would create a table in a SQL database, populate it with data, and then decide you wanted to make a schema change (like adding a string column to your table)? You would have to drop the table, recreate it with the new schema, and the populate it with data *again*.

Django's built in data migrations feature allows you to make scheme changes without having to drop and repopulate your database. Django will do the behind migration work for you.

Even though you don't have any data in your local sqlite database yet, you still have to run the migrations command in order to get your sql database schema created. This way, Django won't throw errors when the code tries to access a table that doesn't exist yet.

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Running the web server

Now you should be able to run the Django development server locally. Run it with the following command:

```bash
python manage.py runserver
```

Then open the link that gets printed to the command line in your browser.

### Done!

That was a lot of steps, but luckily you only have to do them when you first clone down the repo (for the most part).