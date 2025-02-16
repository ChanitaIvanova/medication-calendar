Use venv
source venv/bin/activate

Deactivate venv
deactivate

Install nginx - https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/

Start Nginx: sudo nginx -c /mnt/c/Users/chani/workspace/medication-calendar/proxy/nginx.conf

Stop nginx: sudo pkill -f nginx

To forward MongoDB from port `27017` to `27018`, use the following command in your WSL terminal:

sudo socat TCP-LISTEN:27018,fork TCP:localhost:27017

To stop the forwarding, use:

sudo pkill -f socat

You can then connect to MongoDB using the following connection string in your application or MongoDB Compass:

mongodb://localhost:27018
Make sure that MongoDB is running on port `27017` before executing the `socat` command.