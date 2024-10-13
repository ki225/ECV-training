# WAF Manager
## table of content
* 1 Overview
* 2 Introduction
* 3 Team Member
    * 3.1 Interns
    * 3.2 Mentors
* 4 Background
    * 4.1 Web Application Firewall (WAF) Overview
        * 4.1.1 Key Concepts
        * 4.1.2 Industry Resources
    * 4.2 Current Challenges in WAF Management
        * 4.2.1 Employee Workload Analysis
        * 4.2.2 Limitations of AWS Marketplace Rule Packages
            *  4.2.2.1 Limited Scope of Native AWS Rules
            *  4.2.2.2 Ambiguity in Third-Party Rule Descriptions
            *  4.2.2.3 Inflexibility in Rule Package Structures
            *  4.2.2.4 Customization Challenges
* 5 WAF Manager Solution
    * 5.1 Core Features and Benefits
        * 5.1.1 Cost Reduction Strategies
        * 5.1.2 Time-Saving Mechanisms
        * 5.1.3 AI-Powered Decision Support
    * 5.2 Architecture Overview
        * 5.2.1 System Diagram
        * 5.2.2 Workflow
        * 5.2.3 Component Breakdown
            * 5.2.3.1 User Interface
            * 5.2.3.2 Back-end Server
            * 5.2.3.3 Middleware
            * 5.2.3.4 AI Chatbot Integration
* 6  Cloud Infrastructure
* 7 Front-end Development
* 8 Middleware
    * 8.1 RESTful API Architecture
    * 8.2 Resource and Method Definitions
    * 8.3 Request/Response Formats
* 9 Back-end Systems
    * 9.1 Project Architecture
    * 9.2 AI Chatbot Integration
        * 9.2.1 Environment Setup
        * 9.2.2 Core Lambda Functions
    * 9.3 Terraform Generator
        * 9.3.1 Web Server Configuration (ASGI/Hypercorn)
        * 9.3.2 Web Application Framework (Quart)
    * 9.4 Key Functionalities
        * 9.4.1 Request Validation
        * 9.4.2 Terraform Generation
        * 9.4.3 Process Status Management
        * 9.4.4 S3 Integration
    * 9.5 Performance Optimizations
        * 9.5.1 Asynchronous Processing
    * 9.6 Data Management
        * 9.6.1 S3 Architecture
        * 9.6.2 DynamoDB Integration
    * 9.7 AI Model Integration
        * 9.7.1 OpenAI GPT-4 Implementation
        * 9.7.2 Amazon Bedrock Integration
        * 9.7.3 Prompt Engineering and Management
    * 9.8 Rule Package Management
        * 9.8.1 Testing Methodologies
    * 9.9 Customer Credential Management
        * 9.9.1 IAM Trust Relationships
* 10 Cost Analysis
    * 10.1 Infrastructure Costs
    * 10.2 AI Model Usage Costs
    * 10.3 Overall TCO Considerations
* 11 Impact Assessment
    * 11.1 Efficiency Improvements
    * 11.2 Security Enhancements
    * 11.3 User Feedback and Testimonials
* 12 Conclusion and Future Roadmap
    * 12.1 Key Achievements
    * 12.2 Planned Enhancements
    * 12.3 Long-term Vision
* 13 Appendices
    * A. Project Structure
    * B. API Documentation
    * C. Glossary of Terms
    * D. References and Resources


Overview
---
We provide an intellegent auto-deployment system called "WAF Manager" to help both engineers and customers to save their time by reducing the WAF deploying time.


Introduction
---
During our internship at EcloudValley, we encountered a significant challenge in the realm of web application security: the complex and time-consuming process of setting up a Web Application Firewall (WAF). This task, critical for protecting web applications from various cyber threats, often proves to be a frustrating and resource-intensive endeavor for many organizations.

The difficulties in WAF setup stem from several factors:

1.	Complex Configuration: WAF deployment requires navigating through intricate settings and options, demanding a deep understanding of both web security principles and the specific WAF platform being used.

2.	 Rule Research and Design: Effective WAF protection necessitates extensive research into current threat landscapes and the careful design of rules to counter these threats. This process is both time-consuming and requires specialized knowledge.

3.	Continuous Updates: The ever-evolving nature of cyber threats means that WAF rules and configurations need frequent updates, adding to the ongoing maintenance burden.

4.	Resource Intensiveness: The combination of initial setup and ongoing management often requires dedicated personnel, which can strain resources, especially for smaller organizations.

### Our vision
Recognizing these challenges, we envisioned a solution that could revolutionize the way organizations approach WAF deployment and management. We wanted to create a tool that would:

-	Simplify the WAF setup process, making it accessible to a broader range of users
-	Reduce the time and resources required for effective WAF deployment
-	Leverage cutting-edge AI technology to provide intelligent, context-aware security implementation
-	Offer flexibility to cater to both novice users and experienced security professionals

### Introducing WAF Manager
To address these needs, we developed "WAF Manager" - an innovative solution designed to streamline and enhance the WAF deployment process. WAF Manager serves as a comprehensive platform that combines:

1.	AI-Powered Assistance: Utilizing advanced natural language processing to guide users through WAF setup and provide intelligent rule suggestions.

2.	Intuitive Interface: Offering both an AI-driven conversational mode and a structured manual mode to cater to different user preferences and expertise levels.

3.	Time-Saving Automation: Implementing automated processes to handle repetitive tasks and accelerate the overall deployment timeline.

4.	Adaptive Security: Keep pace with emerging threats and security best practices.

### Key Objectives
By addressing the complexities and inefficiencies in traditional WAF setup processes, WAF Manager stands as a powerful solution for organizations seeking to bolster their web application security posture efficiently and effectively.


Team members
---
### Intern
- Gabriel Yeh
- Kiki Huang
### Mentor
- Greg Ke


Background
---

### Web Application Firewall (WAF) Overview
#### Definition of AWS WAF
Amazon Web Services (AWS) Web Application Firewall (WAF) is a cloud-native security service designed to protect web applications and APIs from a wide array of cyber threats. It offers robust defense mechanisms for critical AWS resources, including Amazon CloudFront distributions, Application Load Balancers, Amazon API Gateway REST APIs, and AWS AppSync GraphQL APIs.

#### Purpose and benefits

1. **Comprehensive Protection**: 
   AWS WAF provides robust security for web applications through advanced features such as IP address blocking and customizable rule sets.

2. **Integrated Monitoring and Analytics**: 
   Seamlessly integrates with AWS monitoring services, enabling real-time analysis of logs and status reports from protected resources.

3. **Customization and Flexibility**: 
   Offers user-defined configuration options tailored to specific security requirements, while also providing pre-configured protection packages for rapid deployment.


#### Components of AWS WAF
*    Web ACLs (Access Control Lists)
*    Rules and Rule Groups
*    IP Sets
*    Regex Pattern Sets


#### Types of Rules
*   Managed Rules:

    Pre-configured rule sets developed by AWS and AWS Marketplace sellers. These rules protect against common web threats and vulnerabilities without requiring extensive security expertise.

*   Custom Rules:

    User-defined rules that allow you to create specific criteria for inspecting web requests. These can be tailored to your application's unique security requirements and business logic.

*   Rate-based Rules:

    Rules that track the rate of requests from individual IP addresses and automatically block IPs when they exceed a specified threshold within a 5-minute time span. These are effective for preventing HTTP flood attacks.


#### Integration with AWS Services
*    Amazon CloudFront
*    Application Load Balancer (ALB)
*    Amazon API Gateway
*    AWS AppSync
*    Amazon Cognito User Pools
*    AWS App Runner

### Current Challenges in WAF Management
#### Employee Workload Analysis
Security engineers tasked with managing Web Application Firewalls face significant time and resource constraints. Their responsibilities typically encompass:

1. **Vulnerability Research**: Continuous monitoring and analysis of emerging threats and attack vectors.
2. **Rule Design and Implementation**: Development of custom rules to address specific security requirements and emerging threats.
3. **Testing and Validation**: Rigorous testing of new and existing rules to ensure efficacy while minimizing false positives.
4. **Performance Optimization**: Balancing security measures with system performance to maintain optimal user experience.

These tasks require a high level of expertise and consume substantial man-hours, potentially leading to resource allocation challenges within security teams.

#### Limitations of AWS Marketplace Rule Packages
While AWS Marketplace offers various rule packages for WAF implementation, several challenges persist:

1. Limited Scope of Native AWS Rules

    AWS-provided rules primarily focus on SQL injection and Cross-Site Scripting (XSS) protection.  This narrow scope necessitates supplementary solutions for comprehensive security coverage.


2. Ambiguity in Third-Party Rule Descriptions

    *   Many third-party rule packages in the AWS Marketplace lack clear, detailed documentation.
    *   Insufficient information hampers customers' ability to make informed decisions about rule selection and implementation.
    *   The absence of transparency in rule logic and coverage areas creates potential security gaps.


3. Inflexibility in Rule Package Structures

    Most marketplace rule packages are designed to address multiple vulnerability types simultaneously. This bundled approach can lead to:
    *   Unnecessary cost implications for customers requiring protection against specific threats.
    *   Potential performance impacts due to the implementation of superfluous rules.

4. Customization Challenges

    *   Adapting generic rules to unique environments often requires additional effort and expertise.





Cloud Infrastructure
---

Front-end Development
---
The front-end is built using Vue.js 3, offering two primary modes of interaction:
1.	AI Mode: A conversational interface leveraging AI to assist users in WAF configuration.
2.	Manual Mode: A structured form interface for direct control over WAF settings.

Key features include:
•	Responsive design for various devices
•	Real-time updates and notifications
•	Markdown rendering for AI responses
•	Progress tracking for WAF deployment



Back-end Systems
---
### Introduction
Our system backend handle the llm AI-agent and auto-deploy service. We use AWS Lambda for connect the user requestand ai-agent api, and use web server and web application for validating json request and generating terraform. 
### AI Chatbot Integration
#### Environment Setup

Configuration requirements
*    Runtime Python 3.9
*    Ephemeral Storage: 512MB
*    Memory: 480MB
*    Timeout: 90 seconds

package requirements
```
langchain
langchain-openai
openai
langchain-core
nvdlib
```
#### Core Lambda Functions
Main function
*   lambda_function.py

Other functions
*   conversation_history.py
    
    make ai-agent reply with history knowledgement.
*   cve_query.py

    it can get cve information according to user's request.
*   model.py

    get human-like response from OpenAI API.
*   prompt.py
    file with different kind of prompts in order to handle different types of requests.
### Terraform Generator
#### Web Server Configuration (ASGI/Hypercorn)
**What is a Web Server?**

A web server is software and hardware that uses HTTP (Hypertext Transfer Protocol) and other protocols to respond to client requests made over the World Wide Web. It hosts and delivers web content, handles incoming network requests, and communicates with server-side applications to generate dynamic content.

**Why use ASGI?**

ASGI (Asynchronous Server Gateway Interface) is a specification for asynchronous web servers and applications in Python. We use ASGI to make programs run asynchronously for several reasons:
1. Improved performance: ASGI allows for concurrent handling of multiple requests, making efficient use of CPU resources.
2. Scalability: Asynchronous processing enables better handling of a large number of simultaneous connections.
3. Real-time capabilities: ASGI supports WebSocket and other long-lived connections, enabling real-time features.
4. Compatibility: It provides a standard interface for asynchronous web applications and frameworks.

**Hypercorn Configuration**
Hypercorn is an ASGI web server based on the sans-io hyper, h11, h2, and wsproto libraries. Key configuration settings include:

Server Socket
- `bind`: The host/address to bind to. [['127.0.0.1:8000']]
- `workers`: The number of workers to spawn and use. [1]
- `worker_class`: The type of worker to use. ["asyncio"]
- `threads`: The number of threads per worker to use. [1]

Security
- `ca_certs`: Path to the SSL CA certificate file
- `certfile`: Path to the SSL certificate file
- `ciphers`: Ciphers to use for the SSL setup
- `keyfile`: Path to the SSL key file
- `cert_reqs`: Whether client certificates are required
- `verify_mode`: SSL verify mode for client certificates

HTTP
- `h11_max_incomplete_size`: The maximum number of bytes to buffer of an incomplete HTTP request
- `h2_max_concurrent_streams`: The maximum number of concurrent HTTP/2 streams
- `h2_max_header_list_size`: The maximum number of items in the HTTP/2 header list
- `h2_max_inbound_frame_size`: The maximum size of an incoming HTTP/2 frame

ASGI
- `root_path`: The root path to mount the ASGI application at
- `limit_concurrency`: The maximum number of concurrent connections
- `backlog`: The maximum number of connections to hold in backlog

Timeouts
- `graceful_timeout`: Time to wait after SIGTERM before force exiting
- `keep_alive_timeout`: Timeout for keep-alive connections
- `worker_timeout`: The maximum time a worker can be silent for

Logging
- `access_log`: The target location for the access log, use `-` for stdout
- `error_log`: The target location for the error log, use `-` for stderr
- `log_config`: The logging configuration file to use
- `log_level`: The logging level to use [INFO]

Development
- `reload`: Enable automatic reloading on code changes
- `use_reloader`: Deprecated alias for `reload`
- `debug`: Enable debug mode, including verbose logging

SSL
- `ssl_keyfile`: Path to the SSL key file
- `ssl_certfile`: Path to the SSL certificate file
- `ssl_version`: The SSL version to use
- `ssl_cert_reqs`: Whether client certificates are required
- `ssl_ca_certs`: Path to the SSL CA certificate file
- `ssl_ciphers`: Ciphers to use for the SSL setup

Performance
- `write_pause`: The pause in seconds between writes to slow clients
- `uvloop`: Enable uvloop usage if available

Miscellaneous
- `pid_path`: Location to write the PID (Program ID) file
- `forwarded_allow_ips`: A list of IPs to trust with proxy headers
- `statsd_host`: The host and port of the statsd server to use
- `statsd_prefix`: Prefix for all statsd messages
- `umask`: The umask to use when spawning workers

**Web Server Running Command**

To start the Hypercorn server with the specified configuration, use the following command:
```
hypercorn server:server --worker-class asyncio --backlog 100 --bind 0.0.0.0:5000 --keep-alive 300
```
   
Command breakdown:
* `server:server`: Specifies the application module and object to be served
* `--worker-class asyncio`: Sets the worker class to asyncio for asynchronous processing
* `--backlog 100`: Sets the maximum number of pending connections to 100
* `--bind 0.0.0.0:5000`: Binds the server to all available network interfaces on port 5000
* `--keep-alive 300`: Sets the keep-alive timeout to 300 seconds (5 minutes)

#### Web Application Framework (Quart)
**What is Web Application?**

A web application is a software program that runs on a web server and is accessed by users through a web browser over the Internet. 

**Why we use Quart?**

Quart is a Fast Python web microframework, we use it consider the following advatages of using it:

1. Asynchronous Architecture

    Leveraging Python's asyncio library, Quart enables non-blocking I/O operations, facilitating efficient concurrent request handling and improved performance for I/O-bound applications. This architecture is particularly well-suited for real-time features and long-running tasks.
2. RESTful API support 
    
    Quart provides robust support for building RESTful APIs, offering intuitive routing, request handling, and JSON processing capabilities.
3. Lightweight and Minimalist
    
    Quart provides flexibility for integrating preferred libraries, simplifies the learning curve, and allows for easy

### Key Functionalities
#### Request Validation

#### Terraform Generation

#### Process Status Management

#### S3 Integration


### Performance Optimizations
#### Asynchronous Processing
### Data Management
#### S3 Architecture
#### DynamoDB Integration

### AI Model Integration
        * 9.7.1 OpenAI GPT-4 Implementation
        * 9.7.2 Amazon Bedrock Integration
        * 9.7.3 Prompt Engineering and Management
### Rule Package Management
        * 9.8.1 Testing Methodologies
### Customer Credential Management
        * 9.9.1 IAM Trust Relationships
