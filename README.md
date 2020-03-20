# EGDAR Sentiment Analysis Data Pipeline on Kubernetes Engine

This Project has 4 Stages
1. Annotation Pipeline
   - This is the starting point for the main pipeline. 
   - It Generates a Database of A Labeled Dataset using Azure Text Analytics API
   - Entire Database is stored in a AWS S3 bucket 
2. Machine Learning Pipeline
   - This is the second pipeline.
   - The Database creates in the Annotation Pipeline is used to train our model
   - The trained model is stored on a S3 bucket
3. REST Flask App
   - The trained model is incubated in a Python Flask REST App
   - The Flask App is tested inside a Docker Container
   - The Docker Container is Deployed on a Google Cloud Kubernetes Engine
4. Inference Pipeline
   - Inference Pipeline is an Automated Sentiment Analysis Pipeline
   - It scrapes EDGAR Earning Call Transcript Data and stores it in the cloud
   - Using the Flask Webapp in Stage 3, It predicts the sentiment of the document.


## Getting Started

These instructions will get you a copy of the project up and running on your Local Environment using Cloud Infrastructure 
```
git clone www.github.com/kashishshah881/ml-as-a-service-pipeline
```

### Prerequisites

```
Python3.7
AWS Account
GCP Account
Microsoft Azure Account
```

### Installing
What things you need to install the software:
```
pip3 install -r requirements.txt
```

### Steps For Running on AWS EC2 Cloud

##### Step 1:
- Create Multiple AWS S3 Buckets
- Configure IAM Role having Full S3 Bucket Access in your local environment. Learn More [Here](https://docs.databricks.com/administration-guide/cloud-configurations/aws/iam-roles.html#step-1-create-an-iam-role-and-policy-to-access-an-s3-bucket)
- Create a GCP Account. Get Started [Here](cloud.google.com)
- Create an Azure Account. Get Started [Here](azure.microsoft.com)
- Request a [Metaflow Sandbox](https://www.metaflow.org/sandbox/) to run your pipeline on AWS Batch.
##### Step 2:
- Once Everything is setup, Configure Metaflow's Sandbox. Run ``` metaflow configure sandbox ``` on CLI. Enter The API Keys from Step 1 <br>
- Configure the input/output buckets on AWS S3 and Enter the bucket name in [Annotation Pipeline](https://github.com/kashishshah881/ml-as-a-service-pipeline/blob/master/Annotation%20Pipeline/index.py#L41-L42) , [ML Pipeline](https://github.com/kashishshah881/ml-as-a-service-pipeline/blob/master/ML%20Pipeline/index.py#L37-L39) , [Inference Pipeline](https://github.com/kashishshah881/ml-as-a-service-pipeline/blob/master/Inference%20Pipeline/index.py#L28-L29)
and [Flask App](https://github.com/kashishshah881/ml-as-a-service-pipeline/blob/master/REST%20Flask%20App/app.py#L26)
- Lastly, add the Azure Api Keys [Here](https://github.com/kashishshah881/ml-as-a-service-pipeline/blob/master/Annotation%20Pipeline/index.py#L21-L22)
##### Step 3:
Run on CLI <br>
- Change the permission of the files
>```chmod a+x Annotation\ Pipeline/index.py ML\ Pipeline/index.py Inference\ Pipeline/index.py ```<br>
- Running the Annotation Pipeline
>```./Annotation\ Pipeline/index.py run --with sandbox ``` <br>
- Running the Machine Learning Pipeline
>```./ML\ Pipeline/index.py run --with sandbox ``` <br>
- Creating a docker container of the flask app <br>
> ```cd REST\ Flask\ App/ ``` <br>
> ```docker build . ``` <br>
> ``` docker login --username=yourhubusername --email=youremail@company.com ``` <br>
> ``` docker push yourhubusername/reponame ``` <br>

##### Step 4:
Once the Dockerized Flask App is in the repo in Step 3,
Create a Kubernetes Cluster on Google Cloud Product and Deploy your Docker File From Hub. Learn More [Here](https://codeburst.io/getting-started-with-kubernetes-deploy-a-docker-container-with-kubernetes-in-5-minutes-eb4be0e96370) <br>
Now Your Flask App Is Up! and Accessible from Anywhere Across The World!

##### Step 5:
Add the required Tickerfile bucket location in [Inference Pipeline](https://github.com/kashishshah881/ml-as-a-service-pipeline/blob/master/Inference%20Pipeline/index.py#L83) <br>
Add the IP Address and Port Number Obtained from The GCP Kubernetes Cluster in [Inference Pipeline](https://github.com/kashishshah881/ml-as-a-service-pipeline/blob/master/Inference%20Pipeline/index.py#L157)











## Built With

* [Flask](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [MetaFlow](https://maven.apache.org/) - Pipeline Framework
* [TensorFlow](https://rometools.github.io/rome/) - Used to generate RSS Feeds


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc




















## SmartyPants

SmartyPants converts ASCII punctuation characters into "smart" typographic punctuation HTML entities. For example:

|                |ASCII                          |HTML                         |
|----------------|-------------------------------|-----------------------------|
|Single backticks|`'Isn't this fun?'`            |'Isn't this fun?'            |
|Quotes          |`"Isn't this fun?"`            |"Isn't this fun?"            |
|Dashes          |`-- is en-dash, --- is em-dash`|-- is en-dash, --- is em-dash|



