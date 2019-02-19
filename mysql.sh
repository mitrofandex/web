sudo /etc/init.d/mysql start
mysql -u root -e "create database PROJECT"
cd ask
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
