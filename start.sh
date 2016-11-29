echo "~ Starting the ayyoa.ml ~"
sudo service start nginx
sudo nohup python /var/www/auth/app.py & # I should probably make this into a systemd script

echo "~ Running on port 80, bb ~"
