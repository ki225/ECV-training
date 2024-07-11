# exam for online courses

# Q3 3. A company is in the process of migrating their applications to AWS. One of their systems requires a database that can scale globally and handle frequent schema changes. The application should not have any downtime or performance issues whenever there is a schema change in the database. It should also provide a low latency response to high-traffic queries. Which is the most suitable database solution to use to achieve this requirement?

- [ ] :An Amazon RDS instance in Multi-AZ Deployments configuration
- [x] : Amazon DynamoDB

# Q4 4. A tech company has a CRM application hosted on an Auto Scaling group of On-Demand EC2 instances. The application is extensively used during office hours from 8 in the morning till 6 in the afternoon. Their users are complaining that the performance of the application is slow during the start of the day but then works normally after a couple of hours. Which of the following can be done to ensure that the application works properly at the beginning of the day?

- [ ] : Configure a Dynamic scaling policy for the Auto Scaling group to launch new instances based on the CPU utilization.
- [x] : Configure a Scheduled scaling policy for the Auto Scaling group to launch new instances before the start of the day.


# Q5 A financial application is composed of an Auto Scaling group of EC2 instances, an Application Load Balancer, and a MySQL RDS instance in a Multi-AZ Deployments configuration. To protect the confidential data of your customers, you have to ensure that your RDS database can only be accessed using the profile credentials specific to your EC2 instances via an authentication token. As the Solutions Architect of the company, which of the following should you do to meet the above requirement?

- [ ] : Create an IAM Role and assign it to your EC2 instances which will grant exclusive access to your RDS instance.
- [x] : Enable the IAM DB Authentication.

# Q7 A retail website has intermittent, sporadic, and unpredictable transactional workloads throughout the day that are hard to predict. The website is currently hosted on-premises and is slated to be migrated to AWS. A new relational database is needed that autoscales capacity to meet the needs of the application's peak load and scales back down when the surge of activity is over. Which of the following option is the MOST cost-effective and suitable database setup in this scenario?

- [ ] : Launch an Amazon Aurora Provisioned DB cluster with burstable performance DB instance class types.
- [x] : Launch an Amazon Aurora Serverless DB cluster then set the minimum and maximum capacity for the cluster.

# Q10 A telecommunications company is planning to give AWS Console access to developers. Company policy mandates the use of identity federation and role-based access control. Currently, the roles are already assigned using groups in the corporate Active Directory. In this scenario, what combination of the following services can provide developers access to the AWS console?

- [ x] : IAM Groups 
- [ ] : IAM Roles
- [ x] : AWS Directory Service AD Connector

# Q12 A startup is using Amazon RDS to store data from a web application. Most of the time, the application has low user activity but it receives bursts of traffic within seconds whenever there is a new product announcement. The Solutions Architect needs to create a solution that will allow users around the globe to access the data using an API.What should the Solutions Architect do meet the above requirement?

- [ ] : Create an API using Amazon API Gateway and use an Auto Scaling group of Amazon EC2 instances to handle the bursts of traffic
- [ ] : Create an API using Amazon API Gateway and use AWS Lambda to handle the bursts of traffic in seconds.


# Q13 An online cryptocurrency exchange platform is hosted in AWS which uses ECS Cluster and RDS in Multi-AZ Deployments configuration. The application is heavily using the RDS instance to process complex read and write database operations. To maintain the reliability, availability, and performance of your systems, you have to closely monitor how the different processes or threads on a DB instance use the CPU, including the percentage of the CPU bandwidth and total memory consumed by each process. Which of the following is the most suitable solution to properly monitor your database?

- [ ] :Use Amazon CloudWatch to monitor the CPU Utilization of your database.
- [ ] : Enable Enhanced Monitoring in RDS.

# Q14 A company needs to design an online analytics application that uses Redshift Cluster for its data warehouse. Which of the following services allows them to monitor all API calls in Redshift instance and can also provide secured data for auditing and compliance purposes?

- [ ] : Amazon Redshift Spectrum
- [ ] : AWS CloudTrailI

> AWS CLoudTrail monitors API.

# Q19 A cryptocurrency trading platform is using an API built in AWS Lambda and API Gateway. Due to the recent news and rumors about the upcoming price surge of Bitcoin, Ethereum and other cryptocurrencies, it is expected that the trading platform would have a significant increase in site visitors and new users in the coming days ahead. In this scenario, how can you protect the backend systems of the platform from traffic spikes?

- [ ] : Switch from using AWS Lambda and API Gateway to a more scalable and highly available architecture using EC2 instances, ELB, and Auto Scaling.
- [ ] : Enable throttling limits and result caching in API Gateway.

# Q21 A company has a cloud architecture that is composed of Linux and Windows EC2 instances that process high volumes of financial data 24 hours a day, 7 days a week. To ensure high availability of the systems, the Solutions Architect needs to create a solution that allows them to monitor the memory and disk utilization metrics of all the instances. Which of the following is the most suitable monitoring solution to implement?

- [ ] : Use the default CloudWatch configuration to EC2 instances where the memory and disk utilization metrics are already available. Install the AWS Systems Manager (SSM) Agent to all the EC2 instances.
- [ ] : Install the CloudWatch agent to all the EC2 instances that gathers the memory and disk utilization data. View the custom metrics in the Amazon CloudWatch console.

>  CloudWatch agent is 