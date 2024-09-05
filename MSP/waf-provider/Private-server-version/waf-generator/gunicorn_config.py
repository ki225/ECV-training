import multiprocessing
import os

# Server socket
bind = "0.0.0.0:5000"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'

# Logging
logfile_base = "/var/log/gunicorn"
os.makedirs(logfile_base, exist_ok=True)

accesslog = f"{logfile_base}/access.log"
errorlog = f"{logfile_base}/error.log"
capture_output = True
loglevel = "info"

# Log format
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'

# Worker management
max_requests = 1000
max_requests_jitter = 50
timeout = 120
keepalive = 2

# Reload the application if any file changes
reload = True

# working directory
chdir = '/home/ec2-user/customers'

# Preload application code
preload_app = True

# Function to generate a per-worker log file name
# def worker_log_filename(worker):
#     return f"{logfile_base}/worker-{worker.id}.log"
def worker_log_filename(worker):
    return f"{logfile_base}/worker-{worker.pid}.log"

# Log handler for capturing worker-specific logs
def worker_exit(server, worker):
    worker_log_file = worker_log_filename(worker)
    if os.path.exists(worker_log_file):
        with open(worker_log_file, 'r') as f:
            server.log.info(f.read())
        os.remove(worker_log_file)

# Lifecycle event handlers
def on_starting(server):
    server.log.info("Starting Gunicorn server...")

def on_reload(server):
    server.log.info("Reloading Gunicorn workers...")

def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal")

def worker_abort(worker):
    worker.log.info("Worker received SIGABRT signal")