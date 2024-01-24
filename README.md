# DevOps_Project-Finance-API
A devops project that presents capabilities of:
1. Writing advanced code in Python and working with API'S
2. Working with Docker and Docker-compose
3. Creating EC2 machines and running the code on them using Terraform
4. Automation of processes with Jenkins

An API server built using flask with 5 endpoints.
The server uses libraries like: Openai and email (among others) in order to add advanced options to the code and failure control.
Endpoints:
1. "/"  -   All Nasdaq stocks and their last change %
2. "/top10"  -   Top 10 preforming stock in the Nasdaq index
3. "/last10"  -   Last 10 preforming stock in the Nasdaq index
4. "/<string:ticker>"  -   Closing prices of a specific ticker over the last 30 days
5. "/info/<string:ticker>"  -   Brief overview of the company's general information (using ChatGPT)
* The server has a swagger-ui endpoint that conveniently explains how the server works

  **How it works?**
The server code written in Python was built into a Docker image and uploaded to Docker Hub.
An additional code file in Python (daily_tests.py) is responsible for accessing the API service and checking that all endpoints working as expected.
This code is also converted into a Docker image and uploaded to Docker Hub.

With the help of a resource.tf file we will create an instance in AWS using the (Iac) methodology.
At this point our instance will have a docker running the docker image of the api server and Genkins installed.

We will create a pipeline in Jenkins according to the jenkins.txt file and everything is ready.

Now our server is running on an aws instance and every day at 5 am Israel time a test of all endpoints and the pulling of the data from the last trading day will be activated
in order to reduce loading times for users during the day.

In case of failure, an email will be sent detailing the fault that occurred.

* It is important to note: you must create an .env file in which you insert your personal keys for Gmail and openai
