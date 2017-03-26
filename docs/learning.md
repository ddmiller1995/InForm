# Backend pre req knowledge

Before you can contribute to the backend, you need to know:

* React
* How to read and write basic Python syntax
* What Django is, how it works, and how we are using it
* What Docker is and how to use it

This document is an attempt to centralize this pre-req knowledge so that if someone on the team doesn't have all of this pre req nice knowledge, they can use this document as a starting point for their research.

## React

It seems like everyone on the team has experience with React, so we should be good with everyone having the basic React knowledge needed in order to contribute.

### container/presentation component pattern

I, Luis, am a huge fan of using the presentation component/container component pattern with my React components. I think it makes the code a lot easier to create and maintain, as well as providing readability and reusability benefits. I think we should totally follow that pattern.

If you don't know what this and you are interested, you should read [this](https://medium.com/@learnreact/container-components-c0e67432e005#.kl8mxicpq) article and then [this](https://medium.com/@dan_abramov/smart-and-dumb-components-7ca2f9a7c7d0#.b8n3tcz4n) article which expands on the previous article. Lots of benefits for doing a little bit of architectural work at the beginning of your React development.

## Python

### Install Python3

For simplicity's sake, let's all use the same Python version. Let's go with the latest Python 3.6. Probably any Python3 version will work, but if you haven't installed Python yet, use [Python3.6](https://www.python.org/downloads/release/python-360/) so we are all on the same page.

### Learning Python

You don't need to spend a lot of time learning Python. You can pick it up pretty quickly on the go.

Still, [this guide](http://www.tutorialspoint.com/python/python_quick_guide.htm) should be a pretty good primer for you to gloss over for understanding Python's basic syntax.

## Learning Django

If you want to contribute to the backend, you should follow the [Django tutorial](https://docs.djangoproject.com/en/1.10/intro/tutorial01/). It is quite lengthy and can easily take you 1-2 hours to complete, but it does a great job of teaching you everything you need to know to develop a web site with Django. It assumes no prior server side web development knowledge, but it's still not dry if you do happen to have prior experience with server side web dev.

If you don't know Python, you can still learn Django and through the tutorial. You just need to have Python installed and then you can just copy and paste their code and run it and you will pick it up pretty quickly, its very naturally readable.

The tutorial is broken up into 7 parts. I recommend doing parts 1-4 as well as 7 to learn everything that you need to know about Django (database modeling, MVC, html templates/partials, and admin interface). It doesn't matter if you skip part 5 and 6 because they are not immediately relevant and the rest of the tutorial doesn't depend on them being completed.

If you need help intsalling python or django feel free to ask Luis. 

## Docker

If you don't know what Docker is or what it does, go through Docker's hello world documentation and that should give you a good overview. Maybe a 10 minute youtube video would help too. We don't all need to know the docker config details, we just all need to know how to us it.