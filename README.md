# kunai
A student management system. Site: https://kunai-app.herokuapp.com/

This is a school management system that uses
[Django](https://www.google.com/search?client=opera&q=django+admin&sourceid=opera&ie=UTF-8&oe=UTF-8) to 
do most of the work of managing students, fee submissions, teacher records etc..

Setting up Kunai is very easy.

## Want to Use?
You can clone this branch and use it right now using any of the methods mentioned below

You can also use the site to login. Here are the details for the admininistrator account:

<details> 
  <summary> <h4>Credentials</h4> </summary>
  
   **Username:** admin
  
   **Password:** 1234
</details>


## Building

It is best to use the python `virtualenv` tool to build locally:

```bash
> virtualenv venv
> source venv/bin/activate
> git clone https://github.com/mar-jac/kunai .
```
Then you navigate to the base directory of the project and install the requirements in your virtual environment

```bash
> cd kunai/kunai
> pip install -r requirements.txt
```
And finally you make migrations to the database, create a super user, and run the server
```bash
> python manage.py makemigrations
> python manage.py migrate
> python manage.py createsuperuser
> python manage.py runserver
```

Then visit `http://localhost:8000` to view the app. Alternatively you
can use foreman and gunicorn to run the server locally

```bash
> foreman start
```
## Building with Docker
First run `docker-compose` to build the container:

```bash
docker-compose build
```

Then, run the following command to create the superuser:

```bash
docker-compose run web python manage.py createsuperuser
```

Finally, the Docker container can be launched with the following command:

```bash
docker-compose up
```

The server should be responding at 127.0.0.1:8000


## Building with Heroku
- [Heroku](https://devcenter.heroku.com/articles/deploying-python)

- [Configuring Django Apps in Heroku](https://devcenter.heroku.com/articles/django-app-configuration)


# Contributing

Just follow the steps above to setup your environment.

## To do

- [x] Manage Students Record in admin
- [x] Submit fees in admin
- [x] Show last submitted fee along with students
- [x] Link Students to different Courses
- [x] Search the record by various fields
- [x] Minimize the number of queries for each view
- [x] Add Teachers Record to admin
- [ ] Add Teachers Salary Record to admin
- [ ] Export Data in csv format from admin
- [ ] Add graph comparing teacher salaries given vs student's fee collected


## Licensing
This Project is Licensed under [GLWTPL](LICENSE)


This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

