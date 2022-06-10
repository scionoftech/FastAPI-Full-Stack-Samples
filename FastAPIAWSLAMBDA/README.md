## Serverless FastAPI with AWS Lambda

Mangum allows us to wrap the API with a handler that we will package and deploy as a Lambda function in AWS.
Then using AWS API Gateway we will route all incoming requests to invoke the lambda and handle the routing internally within our application.

### Install Mangum

```shell
pip install mangum
```

### Setup AWS Resources
This tutorial should fall under the AWS free-tier to create, however continued usage of these resources will have associated costs.

### Create S3 Bucket
* Navigate to S3 in the AWS console and click Create Bucket.
* Give it a name and click Create. In this example we're going to call it serverless-fastapi-lambda-dev

### Upload Zip File
Before we can create the lambda we need to package up our existing FastApi app so it's ready for AWS Lambda.

The lambda won't be running in the virtual environment and will only be running one command (which we will determine when we create it) which will be **main.handler** So we need to install all the dependencies within the zip file since it won't be running pip install like we did locally.

### Package Lambda
Inside your terminal from the root directory of your project, CD into the Python Site Packages folder.

```shell
cd env/lib/python3.7/site-packages
```

Then zip up the contents into the root of the project.

```shell
cd env/lib/python3.7/site-packages
```

```shell
zip -r9 path/to/root/of/project/function.zip
```

CD back into the root of the project.

```shell
cd path/to/root/of/project
```

Next we need to add the contents of the app folder so let's add that into the zip file.

```shell
zip -g ./function.zip -r app
```

### Upload Zip File to S3
* Go inside the S3 bucket you just created and click Upload.
* Add your zip file through the interface that pops up and and click Upload.

### Final Steps
* Create AWS Lambda
* Update Handler
* Test FastAPI Lambda
* Create API Gateway
* Create Resource
* Deploy Lambda Proxy API

### Summary
That's it! We Created a FastAPI application and converted it to an AWS Lambda. Then we setup API Gateway to route all requests to our Lambda proxy.

#### References
- Simple Serverless FastAPI with AWS Lambda - [https://www.deadbear.io/simple-serverless-fastapi-with-aws-lambda/]