#!/usr/bin/env python3
from metaflow import FlowSpec, step
import scrapy
from scrapy.crawler import CrawlerProcess   
from urllib.parse import urlparse
from slugify import slugify
import re
import os
import random
import time
import boto3
import re
import csv
import requests
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import s3fs


########## Never hardcode the keys! Save it in the environment variables. More Info: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
ACCESS_KEY = "" 
SECRET_KEY = ""
SESSION_TOKEN = ""
######################################################

#Authenticate the AWS Credentials

client = authenticate_client()
s3_client = boto3.client('s3', 
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN) 



s3_resource = boto3.resource('s3',  
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN)
s3_fs = s3fs.core.S3FileSystem(anon=False,key=ACCESS_KEY,secret=SECRET_KEY,token=SESSION_TOKEN)



bucket = "" #Enter Bucket name to save the input files
output_bucket  = "" #output bucket to save the labeled data. 


proxies = {
   #Enter your list of proxies here!
}


user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
debug_mode = True


class QuotesSpider(scrapy.Spider):

    name = "quotes"
    custom_settings = {
            'LOG_ENABLED': True,
            'DOWNLOAD_DELAY': 4
    }

'''
// The sample ticker CSV file will be in the format
Stock Ticker
AAPL
AMZN
FB
SNAP
'''
csv_file = csv.reader(s3.open('bucket location for ticker file','rb'))


#loop through csv list
for row in csv_file:
    ticker = row[0]

    def start_requests(self):
        urls = [ 'https://seekingalpha.com/earnings/earnings-call-transcripts/9999' ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_last_page)

    def parse_last_page(self, response):
        data = response.css("#paging > ul.list-inline > li:last-child a::text")
        last_page = data.extract()
        last_page = int(last_page[0])
        for x in range(0, last_page+1):
            page_numbers = random.randint(1,10)
            print("PAGE NUMBERS -------------------"+str(page_numbers))
            if debug_mode == True and x > page_numbers:
                break
            url = "https://seekingalpha.com/symbol/AAPL/earnings/transcripts" % (x)
            yield scrapy.Request(url=url, callback=self.parse)

 
    def parse(self, response):
        print("Parsing results for: " + response.url)
        links = response.css("a[sasource='qp_analysis']")
        links.extract()
        for index, link in enumerate(links):
            url = link.xpath('@href').extract()
            if debug_mode == True and index > 3:
                break
            url = link.xpath('@href').extract()
            data = urlparse(response.url)
            data = data.scheme + "://" + data.netloc + url[0]  
            user_agent = random.choice(user_agent_list)
            print("======------======")
            print("Getting Page:")
            print("URL: " + data)
            print("USER AGENT: " + user_agent)
            print("======------======")
            request = scrapy.Request(data,callback=self.save_contents,headers={'User-Agent': user_agent})
            yield request


    def save_contents(self, response):
        data = response.css("div#content-rail article #a-body")
        data = data.extract()
        data = re.sub("</?[^>]*>", "", data[0])
        url = urlparse(response.url)
        url = url.path
        file_name = slugify(url) + '.txt'
        response = s3_client.put_object(Bucket=bucket,Body=data,Key=file_name)





c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
})




def predict():
    bucket = s3_resource.Bucket(bucket)
    for files in bucket.objects.all():
        body = files.get()['Body'].read()
        sentences = re.split(r' *[\.\?!][\'"\)\]]* *', body.decode())
        data_arr = []
        for i in range(0,len(sentences)): 
                #response = client.analyze_sentiment(inputs=sentences)[i]
                url = 'enter the ip address of your kubernetes app'+'PORT NUMBER'+'/result' #default port 5000
                myobj = {'data': sentences[i]}
                x = requests.post(url, data = json.dumps(myobj))
                body = str(sentences[i])+','+str(x.text)
                response = s3_client.put_object(Bucket=output_bucket,Body=body,Key='output.csv')

                


class LinearFlow(FlowSpec):
    @step
    def start(self):
        self.titles = [1,2,3]
        self.next(self.a, foreach='titles')

    @step
    def a(self):
        self.t=self.a
        c.crawl(QuotesSpider)
        c.start()
        self.next(self.join)


    @step
    def join(self,inputs):
        predict()
        self.next(self.end)

    @step
    def end(self):
        print("its done!!")


if __name__ == '__main__':
    LinearFlow()