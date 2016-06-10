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
3. [Download](http://stackoverflow.com/questions/4604663/download-single-files-from-github) the Vagrantfile and bootstrap.sh 
files from this repository and place them in the directory you created for this project.

##### Serving the project
1. In Terminal/Command Prompt, navigate to the directory containing Vagrantfile and boostrap.sh.
2. Type `vagrant up` to create the virtual machine.
3. This will take some time as the necessary dependencies are installed and the machine is configured.
4. Seriously, give it a while. You may see warnings about deprecation. Ignore those.
5. After the machine has successfully been created, navigate to localhost:5050 in your web browser to access the application.
6. Test out the api endpoints by making requests to localhost:8080 (ex: http://localhost:8080/api/v1/items.json).
