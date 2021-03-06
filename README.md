- [GETTING STARTED](#getting-started)
    - [Motivation](#motivation)
    - [Access the application on the cloud](#access-the-application-on-the-cloud)
    - [Access API documentation](#access-api-documentation)
    - [Obtain access token for different roles](#obtain-access-token-for-different-roles)
    - [Run unit test](#run-unit-test)
- [PROJECT SPECIFICATION](#project-specification)
    - [Description](#description)
    - [Models](#models)
    - [Endpoints](#endpoints)
    - [Roles](#roles)
    - [Tests](#tests)
- [ACCEPTANCE CRITERIA](#acceptance-criteria)
    - [Data Modeling](#data-modeling)
    - [API Architecture and Testing](#api-architecture-and-testing)
    - [Deployment](#deployment)
    - [Code Quality & Documentation](#code-quality--documentation)
- [DEPLOY APPLICATION](#deploy-application)
    - [Set Up Environment](#set-up-environment)
    - [Install Dependencies](#install-dependencies)
    - [Test Application](#test-application)
    - [Deploy Application Locally](#deploy-application-locally)
    - [Deploy Application On Cloud (Heroku)](#deploy-application-on-cloud-heroku)
- [AUTH0 AUTHENTICATION AND RBAC](#auth0-authentication-and-rbac)
  <br />

# GETTING STARTED

### Motivation

This project allow me to apply all my knowledge and lessons learned into action. I have a clear big picture of my goals by reading thoroughly project specification, noting down acceptance criteria, preparing list of items to be done and tracking my own progress everyday. The completion of this project will be my proud showcase of my new skillset to the potential employer.

### Access the application on the cloud

```
https://my-casting-agency-2021.herokuapp.com/
```

### Access API documentation

```
https://my-casting-agency-2021.herokuapp.com/apidocs/
```

### [Obtain access token for different roles](#auth0-authentication-and-rbac)

### [Run unit test](#test-application)

<br />
# PROJECT SPECIFICATION

### Description

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

### Models

- Movies with attributes title and release date
- Actors with attributes name, age and gender

### Endpoints

- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/

### Roles

- Casting Assistant
  - Can view actors and movies
- Casting Director
  - All permissions a Casting Assistant has
  - Add or delete an actor from the database
  - Modify actors or movies
- Executive Producer
  - All permissions a Casting Director has
  - Add or delete a movie from the database

### Tests

- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role
  <br />

# ACCEPTANCE CRITERIA

### Data Modeling

1. Architect relational database models in Python

   - [x] Use of correct data types for fields
   - [x] Use of primary and optional foreign key ids

2. Utilize SQLAlchemy to conduct database queries

   - [x] Does not use raw SQL or only where there are not SQLAlchemy equivalent expressions
   - [x] Correctly formats SQLAlchemy to define models
   - [x] Creates methods to serialize model data and helper methods to simplify API behavior such as insert, update and delete.

### API Architecture and Testing

1.  Follow RESTful principles of API development

    - [x] RESTful principles are followed throughout the project, including appropriate naming of endpoints, use of HTTP methods GET, POST, PATCH and DELETE
    - [x] Routes perform CRUD operations

2.  Structure endpoints to respond to four HTTP methods, including error handling

    - [x] Specifies endpoints and behaviour for at least:
      - Two GET requests
      - One POST request
      - One PATCH request
      - One DELETE request
    - [x] Utilize the `@app.errorhandler` decorator to format error responses as JSON objects for at least four different status codes

3.  Enable RBAC

    - [x] Project includes a custom @requires-auth decorator that
      - Get the authorization header from the request
      - Decode and verify JWT using the Auth0 secret
      - Take an argument to describe the action, i.e. `@require_auth('create:drink')`
      - Raise an error if
        - The token is expired
        - The claims are invalid
        - The token is invalid
        - The JWT does not contain the proper action
    - [x] Project includes at leat two different roles that have distinct permissions for actions. These roles and permissions are clearly defined int the project README

4.  Demonstrate validity of API behavior

    - [x] Includes at least one test for expected success and error behaviour for each endpoint using the unittest library
    - [x] Includes tests demonstrating RBAC, at least two per role

 <br/>

### Deployment

1. Application is hosted live at student provided URL

   - [x] API is hosted live via Heroku
   - [x] URL is provided in project README
   - [x] API can be accessed by URL and requires authentication

2. Includes instructions to set up authentication
   - [x] Instructions are provided in README for setting up authentication so reviewers can test endpoints at live application endpoint

### Code Quality & Documentation

1. Write clear, concise and well documented code
   The code adheres to the PEP 8 style guide and follows common best practices, including:
   - [x] Variable and function names are clear.
   - [x] Endpoints are logically named.
   - [x] Code is commented appropriately.
   - [x] Secrets are stored as environment variables.
2. Project demonstrates reliability and testability
   - [x] Application can be run with no errors and responds with the expected results.
   - [x] API test suite for endpoints and RBAC behavior runs without errors or failures
3. Project demonstrates maintainability

   - [x] Variable names are logical, code is DRY and well-commented where code complexity makes them useful

4. Project includes thorough documentation
   Project includes an informative README

   - [x] Motivation for project
   - [x] Project dependencies, local development and hosting instructions,
   - [x] Detailed instructions for scripts to install any project dependencies, and to run the development server.
   - [x] Documentation of API behavior and RBAC controls

# DEPLOY APPLICATION

### Set Up Environment

### Install Dependencies

### Test Application

To ensure the application performs as expected for all users, we must ensure the application works for all supported roles. There are four roles in our application: `Casting Assistant`, `Casting Director`, `Executive Producder` and `Public`. `Public` account means there is no access token provided for a request and the application must reject all requests from `Public` account.

- Step 1: Follow [these instructions](#auth0-authentication) to retrieve access token
- Step 2: Set environment variable `TEST_TOKEN` to the retrieved token value  
  For example,
  ```bash
  export TEST_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5oeWxCOTlDSndqcGh6c294ZEFNSSJ9.eyJpc3MiOiJodHRwczovL2ZyYW5rbmd1eWVudmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwYWE0MjA2YWU1NGIzMDA2OThmZTM5NiIsImF1ZCI6ImF1dGgiLCJpYXQiOjE2MjE4NjUwMTQsImV4cCI6MTYyMTg3MjIxNCwiYXpwIjoib29uUjFWeHg2YlBqSmFrTE93V3FIaXhRSjVjaXNTakciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJjcmVhdGU6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiXX0.vJB4jyjr6kxkaDkhHWL5jTv-O6-Nbw35hBjE7H25jkQxJwzeYl2-vkOS2NKAefVFsaPKWtde7nlDHbF7yMZ3-ZJDcIWAVt9TOEMZZYiUHHPwtYSleWGmvwufmCNlDYxpFXQiutc0207a3X2lB-5VPyKzMwV0mTt5JSHWTFCZ3s0jVFBzL2M5tOcOimX2m5mwoI5TL3P9aNuSVk0Q4OG-5b4CHoOSQy0n4xcaHLH4oKaTKiwjfseaJO8sjdJPWDMdtLNohe9il899L0iGpNWcpOWoMtv6jANtZ7klIBvsdTtDYMMRRVjogdJl1TpEPPzch2PaI5sAWhBRFOc-GT-HeQ"
  ```
- Step 3: Set environment variable `TEST_ROLE` to role that access token belongs to

  - `""` represents `Public` account
  - `casting_assistant` represents `Casting Assistant` account
  - `casting_director` represents `Casting Director` account
  - `executive_producer` represents `Executive Producer` account  
    For example,
    ```bash
    export TEST_ROLE="executive_producer"
    ```

- Step 4: From the project folder, run

  ```bash
  pytest
  ```

  <br/>

### Deploy Application Locally

From the project folder, run

```bash
bash run.sh
```

> :exclamation: This script will export all necessary environment variables used only for the evaluation of the application. For production, we will save all these environment variables in `.env` or in Heroku environment variables

### Deploy Application On Cloud (Heroku)

1. [Install Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

2. [Log in Heroku](https://devcenter.heroku.com/articles/heroku-cli#getting-started)

3. [Create a new app](https://devcenter.heroku.com/articles/creating-apps)

4. [Deploy code](https://devcenter.heroku.com/articles/git#deploying-code)
   For example,

   Push code from branch develop

   ```bash
   git push heroku develop:main
   ```

   Push code from branch main

   ```bash
   git push heroku main:main
   ```

5. [Create environment variables](https://devcenter.heroku.com/articles/config-vars)
   For example

   ```bash
   AUTH0_DOMAIN="franknguyenvd.au.auth0.com"
   AUTH0_CLIENT_ID="oonR1Vxx6bPjJakLOwWqHixQJ5cisSjG"
   AUTH0_IDENTIFIER="auth"
   AUTH0_ALGORITHM="RS256"
   ```

6. Open the app from the terminal
   ```bash
   heroku open
   ```

# AUTH0 AUTHENTICATION AND RBAC

1. RBAC Accounts

List of accounts registered on Auth0

| Account            | Email                          | Password  |
| ------------------ | ------------------------------ | --------- |
| Casting Assistant  | casting_assistant@udacity.com  | @Udacity1 |
| Casting Director   | casting_director@udacity.com   | @Udacity1 |
| Executive Producer | executive_producer@udacity.com | @Udacity1 |

Where

- Casting Assistant can access:
  - GET /movies
  - GET /actors
- Casting Director can access
  - POST /actors
  - GET /actors
  - PATCH /actors
  - DELETE /actors
  - GET /movies
  - PATCH /movies
- Executive Producer can access
  - POST /actors
  - GET /actors
  - PATCH /actors
  - DELETE /actors
  - POST /movies
  - GET /movies
  - PATCH /movies
  - DELETE /movies

2. Get JWT Token

To retrieve access token, please click [here](https://franknguyenvd.au.auth0.com/authorize?audience=auth&response_type=token&client_id=oonR1Vxx6bPjJakLOwWqHixQJ5cisSjG&redirect_uri=http://127.0.0.1:8000/) and log in with one of the above account credential
