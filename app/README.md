Create venv 
python3.12 -m venv venv

Use venv
source venv/bin/activate

Deactivate venv
deactivate

Install nginx - https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/

Start Nginx: sudo nginx -c /mnt/c/Users/chani/workspace/medication-calendar/proxy/nginx.conf

Stop nginx: sudo pkill -f nginx