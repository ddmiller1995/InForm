# InForm

This repo contains the source code for the backend and the frontend.

## Backend

The backend will be a Django web server. It will either server as an API for a standalone frontend server to consume, or it will also serve the front end itself.

### Learning Python

You don't need to spend a lot of time learning Python. You can pick it up pretty quickly on the go.

Still, [this guide](http://www.tutorialspoint.com/python/python_quick_guide.htm) should be a pretty good primer for you to gloss over for understanding Python's basic syntax.

### Learning Django

If you want to contribute to the backend, you should follow the [Django tutorial](https://docs.djangoproject.com/en/1.10/intro/tutorial01/). It is quite lengthy and can easily take you 1-2 hours to complete, but it does a great job of teaching you everything you need to know to develop a web site with Django. It assumes no prior server side web development knowledge, but it's still not dry if you do happen to have prior experience with server side web dev.

If you don't know Python, you can still learn Django and through the tutorial. You just need to have Python installed and then you can just copy and paste their code and run it and you will pick it up pretty quickly, its very naturally readable.

The tutorial is broken up into 7 parts. I recommend doing parts 1-4 as well as 7 to learn everything that you need to know about Django (database modeling, MVC, html templates/partials, and admin interface). It doesn't matter if you skip part 5 and 6 because they are not immediately relevant and the rest of the tutorial doesn't depend on them being completed.

If you need help intsalling python or django feel free to ask Luis. 

### Setup for development

#### Install Python3

For simplicity's sake, let's all use the same Python version. Let's go with the latest Python 3.6. Probably any Python3 version will work, but if you haven't installed Python yet, use [Python3.6](https://www.python.org/downloads/release/python-360/) so we are all on the same page.

#### Install dependencies with pip

Navigate to the project root in the command line and then run the following:

```bash
# after cd to project root
pip install -r requirements.txt
```

For people with a node background, requirements.txt is analogous to package.json, and pip is analogous to npm.

This command will install all of our project's 3rd party module dependencies (and the correct versions) in one command. We need to keep track of these dependencies in this file so our project is portable. This will make life easier for deployment and for whoever ends up maintaining the project later on down the road. Having a requirements.txt file is a common practice in Python.

If you want to add a dependency to this project later, you can easily install that dependency locally and then run 

```bash

pip freeze > requirements.txt
```

to update the requirements file. Make sure to commit any changes to the requirements file.

### How to run the Django development server

```bash
python manage.py runserver
```

Then open the link that gets printed to the command line in your browser.