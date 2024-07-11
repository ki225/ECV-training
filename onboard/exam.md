# exam for online courses
# Q1 An online medical system hosted in AWS stores sensitive Personally Identifiable Information (PII) of the users in an Amazon S3 bucket. Both the master keys and the unencrypted data should never be sent to AWS to comply with the strict compliance and regulatory requirements of the company. Which S3 encryption technique should the Architect use?

- [ ] Use S3 client-side encryption with a KMS-managed customer master key.
- [x] Use S3 client-side encryption with a client-side master key.

> With KMS, we will store the master key. However, the question ask for "Both the master keys and the unencrypted data should never be sent to AWS," so we cannot choose that.
> 

# Q3 3. A company is in the process of migrating their applications to AWS. One of their systems requires a database that can scale globally and handle frequent schema changes. The application should not have any downtime or performance issues whenever there is a schema change in the database. It should also provide a low latency response to high-traffic queries. Which is the most suitable database solution to use to achieve this requirement?

- [ ] : An Amazon RDS instance in Multi-AZ Deployments configuration
- [x] : Amazon DynamoDB

> Amazon DynamoDB can automatically replicate data across multiple AWS regions. It also provides fast, local read and write performance for globally distributed applications.
> 
> RDS Multi-AZ provides high availability within a single region but doesn't natively support global scalability.


# Q4 4. A tech company has a CRM application hosted on an Auto Scaling group of On-Demand EC2 instances. The application is extensively used during office hours from 8 in the morning till 6 in the afternoon. Their users are complaining that the performance of the application is slow during the start of the day but then works normally after a couple of hours. Which of the following can be done to ensure that the application works properly at the beginning of the day?

- [ ] : Configure a Dynamic scaling policy for the Auto Scaling group to launch new instances based on the CPU utilization.
- [x] : Configure a Scheduled scaling policy for the Auto Scaling group to launch new instances before the start of the day.

> There are only 4 types of scaling
> - Target tracking scaling
> - Step Scaling
> - Simple Scaling
> - Scheduled Scaling: Scheduled scaling allows you to plan and manage capacity changes in advance to meet predictable load changes.

# Q5 A financial application is composed of an Auto Scaling group of EC2 instances, an Application Load Balancer, and a MySQL RDS instance in a Multi-AZ Deployments configuration. To protect the confidential data of your customers, you have to ensure that your RDS database can only be accessed using the profile credentials specific to your EC2 instances via an authentication token. As the Solutions Architect of the company, which of the following should you do to meet the above requirement?

- [ ] : Create an IAM Role and assign it to your EC2 instances which will grant exclusive access to your RDS instance.
- [x] : Enable the IAM DB Authentication.

> IAM database authentication is supported by Amazon RDS for MySQL and PostgreSQL. 
> 
> If we use the upper option, applications on the EC2 instance can use the role's permissions without managing AWS credentials, and it does not reach the requirements from questions.


# Q6 The company that you are working for has a highly available architecture consisting of an elastic load balancer and several EC2 instances configured with auto-scaling in three Availability Zones. You want to monitor your EC2 instances based on a particular metric, which is not readily available in CloudWatch. Which of the following is a custom metric in CloudWatch which you have to manually set up?

- [ ] : Network packets out of an EC2 instance
- [x] : Memory Utilization of an EC2 instance


# Q7 A retail website has intermittent, sporadic, and unpredictable transactional workloads throughout the day that are hard to predict. The website is currently hosted on-premises and is slated to be migrated to AWS. A new relational database is needed that autoscales capacity to meet the needs of the application's peak load and scales back down when the surge of activity is over. Which of the following option is the MOST cost-effective and suitable database setup in this scenario?

- [ ] : Launch an Amazon Aurora Provisioned DB cluster with burstable performance DB instance class types.
- [x] : Launch an Amazon Aurora Serverless DB cluster then set the minimum and maximum capacity for the cluster.
 
> ?

# Q10 A telecommunications company is planning to give AWS Console access to developers. Company policy mandates the use of identity federation and role-based access control. Currently, the roles are already assigned using groups in the corporate Active Directory. In this scenario, what combination of the following services can provide developers access to the AWS console?

- [ x] : IAM Groups 
- [ ] : IAM Roles
- [ x] : AWS Directory Service AD Connector

> because the roles are already assigned using groups in the corporate Active Directory, we dont need to care about IAM role.

# Q12 A startup is using Amazon RDS to store data from a web application. Most of the time, the application has low user activity but it receives bursts of traffic within seconds whenever there is a new product announcement. The Solutions Architect needs to create a solution that will allow users around the globe to access the data using an API.What should the Solutions Architect do meet the above requirement?

- [ ] : Create an API using Amazon API Gateway and use an Auto Scaling group of Amazon EC2 instances to handle the bursts of traffic
- [x] : Create an API using Amazon API Gateway and use AWS Lambda to handle the bursts of traffic in seconds.

> Lambda is generally better because it can instantly scale to handle the burst without any pre-warming or scaling lag.

# Q13 An online cryptocurrency exchange platform is hosted in AWS which uses ECS Cluster and RDS in Multi-AZ Deployments configuration. The application is heavily using the RDS instance to process complex read and write database operations. To maintain the reliability, availability, and performance of your systems, you have to closely monitor how the different processes or threads on a DB instance use the CPU, including the percentage of the CPU bandwidth and total memory consumed by each process. Which of the following is the most suitable solution to properly monitor your database?

- [ ] : Use Amazon CloudWatch to monitor the CPU Utilization of your database.
- [x] : Enable Enhanced Monitoring in RDS.

> The first option doesn't offer process-level or thread-level granularity by default. 

# Q14 A company needs to design an online analytics application that uses Redshift Cluster for its data warehouse. Which of the following services allows them to monitor all API calls in Redshift instance and can also provide secured data for auditing and compliance purposes?

- [ ] : Amazon Redshift Spectrum
- [x] : AWS CloudTrailI

> AWS CLoudTrail monitors API.

# Q19 A cryptocurrency trading platform is using an API built in AWS Lambda and API Gateway. Due to the recent news and rumors about the upcoming price surge of Bitcoin, Ethereum and other cryptocurrencies, it is expected that the trading platform would have a significant increase in site visitors and new users in the coming days ahead. In this scenario, how can you protect the backend systems of the platform from traffic spikes?

- [ ] : Switch from using AWS Lambda and API Gateway to a more scalable and highly available architecture using EC2 instances, ELB, and Auto Scaling.
- [x] : Enable throttling limits and result caching in API Gateway.

> user can use API Gateway Throttling to set up request rate limits (throttling) at the API Gateway level.
> 
> It is not necessary to change to use ec2 because both ec2 and lambda can be scalable and available.


# Q21 A company has a cloud architecture that is composed of Linux and Windows EC2 instances that process high volumes of financial data 24 hours a day, 7 days a week. To ensure high availability of the systems, the Solutions Architect needs to create a solution that allows them to monitor the memory and disk utilization metrics of all the instances. Which of the following is the most suitable monitoring solution to implement?

- [ ] : Use the default CloudWatch configuration to EC2 instances where the memory and disk utilization metrics are already available. Install the AWS Systems Manager (SSM) Agent to all the EC2 instances.
- [x] : Install the CloudWatch agent to all the EC2 instances that gathers the memory and disk utilization data. View the custom metrics in the Amazon CloudWatch console.

>  CloudWatch agent just like a packet for EC2. It can get other detail msg about ec2 and send them to cloudwatch, e.g. ec2's memory, …
> 
> It can also be used for hybrid architecture.

# Q22 A web application is using CloudFront to distribute their images, videos, and other static contents stored in their S3 bucket to its users around the world. The company has recently introduced a new member-only access to some of its high quality media files. There is a requirement to provide access to multiple private media files only to their paying subscribers without having to change their current URLs. Which of the following is the most suitable solution that you should implement to satisfy this requirement?

- [ ] : Configure your CloudFront distribution to use Match Viewer as its Origin Protocol Policy which will automatically match the user request. This will allow access to the private content if the request is a paying member and deny it if it is not a member.
- [x] : Use Signed Cookies to control who can access the private files in your CloudFront distribution by modifying your application to determine whether a user should have access to your content. For members, send the required Set-Cookie headers to the viewer which will unlock the content only to them.

> The "Match Viewer" setting does not provide any authentication or authorization capabilities. It is specifically about protocol matching (HTTP vs HTTPS).
> 
> using Signed Cookies will add token in cookie for authentication


# Q23 23. A suite of web applications is hosted in an Auto Scaling group of EC2 instances across three Availability Zones and is configured with default settings. There is an Application Load Balancer that forwards the request to the respective target group on the URL path. The scale-in policy has been triggered due to the low number of incoming traffic to the application. Which EC2 instance will be the first one to be terminated by your Auto Scaling group?

- [ ] : The EC2 instance which has the least number of user sessions
- [x] : The EC2 instance launched from the oldest launch configuration

> In [official document](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-instance-termination.html), it describes "If you did not assign a specific termination policy to the group, Amazon EC2 Auto Scaling uses the default termination policy. It selects the Availability Zone with two instances, and terminates the instance that was launched from a launch configuration, a different launch template, or **the oldest version** of the current launch template."


# Q25 A Forex trading platform, which frequently processes and stores global financial data every minute, is hosted in your on-premises data center and uses an Oracle database. Due to a recent cooling problem in their data center, the company urgently needs to migrate their infrastructure to AWS to improve the performance of their applications. As the Solutions Architect, you are responsible in ensuring that the database is properly migrated and should remain available in case of database server failure in the future. Which of the following is the most suitable solution to meet the requirement?
- [ ] : Convert the database schema using the AWS Schema Conversion Tool and AWS Database Migration Service. Migrate the Oracle database to a non-cluster Amazon Aurora with a single instance.
- [x] : Create an Oracle database in RDS with Multi-AZ deployments.

> Aurora is a Cluster-based architecture. It consists of one or more database instances, so it has high availability.
> 
> For availability, one of the way is to make resources be deplyed in Multi-AZ.