[![Python CI](https://github.com/cyrilmcshow/python-project-83/actions/workflows/linter.yml/badge.svg)](https://github.com/cyrilmcshow/python-project-83/actions/workflows/linter.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/7b4dc61e32009f10cf8d/maintainability)](https://codeclimate.com/github/cyrilmcshow/python-project-83/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/7b4dc61e32009f10cf8d/test_coverage)](https://codeclimate.com/github/cyrilmcshow/python-project-83/test_coverage)

### [Check out in action](https://page-analyzer-79z7.onrender.com)

### About project:
This app helps analyze SEO usability of website. It's able to find main headline, title and description.

### What is SEO usability and why it is important:
SEO website usability refers to the ability of a website to be optimized for search engines such as Google, Bing, and Yandex. It involves meeting certain requirements that help search engines understand the content of the website and display it in search results. These requirements include the use of keywords, metadata, page titles, and other factors that help search engines understand what the website offers. SEO website usability is important because it helps to improve the visibility of the website in search engines. If a website does not meet the requirements of search engines, it may not be visible enough to users who are searching for information related to its topic. This can lead to a decrease in traffic to the website and a decrease in potential customers. On the other hand, if a website meets the requirements of search engines, it may be better visible in search results, which can lead to an increase in traffic to the website and an increase in potential customers.

## Requirements:
- Python >=3.10
- Pip
- Poetry
- PostgreSQL

## Installation
1. Clone this repository to your computer by command:
```sh
   git clone git@github.com:Agrarox666/python-project-83.git
```

## Secret Key
1. Create a file for environment variables in the page_analyzer .env directory with the following information
```bash
DATABASE_URL=postgresql://{username}:{password}@{host}:{port}/{databasename}  
SECRET_KEY='{your secret key}'
```

## Quick start
1. Install poetry and db (postgresql) on your PC and by command (from the main directory):
```sh
   make build
```
2. Start gunicorn server by command:
```sh
   make start
```
A simple page analyzer is running on your computer and ready to go!

## If you want to test the application
1. Replace the string in the dump_db.sh and restore_db.sh files:
```sh
   postgresql://{username}:{password}@{host}:{port}/{databasename}
```
2.  Run the tests by command:
```sh
   make test
```
