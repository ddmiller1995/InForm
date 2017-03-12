# Project architecture

## Backend

For the backend we are using Django for our server side web framework. 

### Database

Django will be the only one directly interfacing with our database.

It's true that our frontend will need to fetch data from the database, but it will do so indirectly by accessing the API that the backend provides.

We can probably just use a single file sqlite database, since it is such a small scale project that there is very little concurrency/scale risk. If we want to, we can also set up a more robust MySQL database.

MySQL will be more powerful, but also may introduce more points of failure, since MySQL is essentially another server.

### What will Django serve?

Django will serve two types of web requests

#### 1) The front end

When the user visits our root URL (e.g. foycapstone.com/), Django will serve an HTML page.

Embedded in this HTML page will be the JS bundle, which will include our front end code and any other JS dependencies we have. 

This page will become a React single page application. React will manage state, routes, presentation, and business logic.

Django will manage the data layer.

Another way of thinking about this is that our system will implement the [layered 3-tier software architecture](http://www.hanselman.com/blog/AReminderOnThreeMultiTierLayerArchitectureDesignBroughtToYouByMyLateNightFrustrations.aspx).

Our React front end will handle the presentation tier and the application tier.
Our Django back end will handle the data tier.

#### 2) API calls

The other kind of web request that our Django server will handle is JSON API calls from the front end. This is how Django will implement the data tier of our 3-tier architecture.

For example, for the youth tracker [home page](https://tessaev1.wixsite.com/youthhaven) the front end needs to fetch a list of rows from the youth table in the database.

The front end will make a web request to the backend like the following:

```javascript
fetch('/api/fetchYouth')
.then(response => return response.json())
.then(youthArray => {
  for (let youth of youthArray) {
     console.log(`Name: ${youth.name}`);
  }
});
```

## Frontend

For the frontend, we are using React.

### How is the front end served?

The front end will be served by a somewhat complex process of bundling the JS dependencies and having the back end serve them.

