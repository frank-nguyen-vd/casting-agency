# PROJECT: CASTING AGENCY

&nbsp;
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
\
\
&nbsp;

# DEPLOY HEROKU APPLICATION
If you want to deploy code to Heroku from a non-main branch of your local repository (for example, testbranch), use the following syntax to ensure it is pushed to the remote’s main branch:
```bash
git push heroku testbranch:main
```