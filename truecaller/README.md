## Truecaller

### How to setup project

1. create virtualenv and install packages from requirement.txt
(please refer internet on how to create virtualenv)

2. as my project uses mysql, setup mysql user and db with the below credentials
  > database name: truecaller <br />
    username: one    <br />
    password: one  <br />
    host:localhost <br />
    port: 3306

3. use the below command to import the mysql dump into your database
> mysql -u one -p truecaller<truecaller_dump.sql <br />
one



4. use the below command to run server
> python manage.py runserver



5. to run unit tests. simply run
  > python manage.py tests

  _NOTE: as authorization oauth server is different from my client server. python dev server should be running otherwise the tests would fail to authenticate user_. it is written in such a way so that it can broken into microservices and deployed separately

<hr />

### API Operations

1. register a user
~~~~
POST /authentication/register
{
  "phone_number":"",
  "name":"",
  "email":"",
  "password":""
}
~~~~
2. login user
~~~~
POST /authentication/user_login
{
  "username":"",
  "password":""
}
~~~~
3. logout user
~~~~
POST /authentication/user_logout
{
  "token":""
}
~~~~
4. search by name
~~~~
GET /search?name<name>
~~~~
5. search by phonenumber
~~~~
GET /search?phone_number<phone_number>
~~~~
6. spam a number
~~~~
POST /mark_spam
{
  "phone_number":"<phone_number>"
}
~~~~

_NOTE: other than user management urls, all other urls would require you to add oauth token in header in form_
> Authorization : Bearer <your_token>
