# Store App Backend Project
This project fulfills the requirement for the Item Catalog project, which is a part of Udacity's Full Stack Web Development
nano-degree.

The goal of the project is to develop an application that provides a list of items within a variety of 
categories as well as provide a user registration and authentication system. Registered users will have 
the ability to post, edit and delete their own items.

I chose to create a generic store inventory that allows users to add their own listings of items, along with the item's 
associated cost, stock, description, and optional item image. If an image is not provided, a generic placeholder is used 
instead.

### Setting up the project

##### Prerequisites
1. [Download](https://www.virtualbox.org/wiki/Downloads) and install [VirtualBox](https://www.virtualbox.org/) if it isn't already.
2. [Download](https://www.vagrantup.com/downloads.html) and install [Vagrant](https://www.vagrantup.com) if it isn't already.
3. [Download](http://stackoverflow.com/questions/4604663/download-single-files-from-github) the Vagrantfile and bootstrap.sh from this repository and place them in the directory you created for this project.

##### Creating the Virtual Machine
1. Using Terminal or Command Prompt, navigate to the directory containing the Vagrantfile.
2. Type `vagrant up` to begin the creation of the virtual machine.
3. Ensure that ports 5050 and 8080 on your host machine are not being used by other applications.
4. Once the creation of the virtual machine has completed, type `vagrant ssh` to connect to the machine.

##### Setting up the project
The following commands will need to be entered in the order they appear (Copy/Paste them in):

1. Prepare to update our current version of Python: `cd /usr/src/`
2. Download Python 2.7.10 and unpack it: `sudo wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz && sudo tar xzf Python-2.7.10.tgz`
3. Move into the new Python directory and configure: `cd Python-2.7.10 && sudo ./configure`
4. `sudo make altinstall`
5. Move back to our directory to begin setting up the project directories: `cd`
6. Download the backend project: `git clone https://github.com/jwelker110/store_backend.git`
7. Move into the project: `cd store_backend`
8. Switch to the current branch: `git checkout udacity`
9. Create the virtual environment: `virtualenv --python=/usr/bin/python2.7 store-env`
10. Activate the virtual environment so we can install our dependencies: `source store-env/bin/activate`
11. Install our dependencies: `pip install -r requirements.txt`
12. Install uWSGI using pip: `pip install uwsgi`
13. Move into the project's config directory: `cd store_app/config`
14. We can use the example as our secret: `mv config_example.py config_secret.py`
15. Create two files that typically are both required, however only one of them is 'required': `touch client_secret.json secret_keys.json`
16. Give ourselves a generic JWT Cipher Key (This would be changed in prod): `echo "{\"JWT_CIPHER\": \"this is the JWT cipher\"}" >> secret_keys.json`
17. Begin setting up uWSGI according to [Digital Ocean's](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04) tutorial: `cd /home/vagrant/store_backend/`
18. We want our application to start when the machine is in the 'on' state so we move the conf file into the init directory: `sudo mv store_app.conf /etc/init/`
19. Start the app up: `sudo start store_app`
20. Prepare Nginx by first renaming the default site: `sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default_copy`
21. Move into our project's directory: `cd /home/vagrant/store_backend/`
22. Move the provided Nginx site config to the sites-available directory: `sudo mv store_app_server /etc/nginx/sites-available/`
23. Enable our site: `sudo ln -s /etc/nginx/sites-available/store_app_server /etc/nginx/sites-enabled`
24. Get started on the frontend: `cd /home/vagrant/`
25. Grab the frontend repo: `git clone https://github.com/jwelker110/store_frontend.git`
26. Move into the repo: `cd store_frontend`
27. Checkout the latest branch: `git checkout udacity`
28. Let's get Nodejs installed (We don't want the latest version): `curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash - `
29. Continue: `sudo apt-get install -y nodejs`
30. Sweet, let's install [npm](https://www.npmjs.com/): `sudo npm install -g npm`
31. Alrighty here comes the long, boring part: installing the npm packages: `npm install`
32. Once the previous step finally completes, let's install our dev tools: `sudo npm install -g yo gulp bower`
33. We have [bower](https://bower.io/), let's install the dependencies: `bower install`
34. FINALLY!! We're ready to build the project from the source: `gulp`
35. Finish it all off by ensuring Nginx is up-to-date: `sudo service nginx restart`


