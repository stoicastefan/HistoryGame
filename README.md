## Tools used for the game development
HistoryGame is a web application built with Python, Flask, JavaScript, and Flask_SQLAlchemy. Python and Flask were used for the server-side, while JavaScript was used for the client-side. Flask_SQLAlchemy was used for interacting with the database. HTML and CSS were used for the project to structure and style the web pages. HTML provided the backbone of the pages, while CSS enabled the creation of the design. 

## Using the SSH key in Pycharm
This is a tutorial list that provides step-by-step instructions for generating and using SSH keys with GitHub and PyCharm. SSH keys are a secure way to authenticate with remote servers, and they can be used to securely access GitHub repositories from PyCharm. The tutorials in this list provide detailed instructions for generating an SSH key using Git Bash or GitHub's website, and then using the key to access GitHub repositories from PyCharm. Whether you are new to using SSH keys or are looking to set up SSH key authentication for the first time, these tutorials will guide you through the process.
Open Git Bash on your computer (or any terminal if you're not on Windows).
1. Type the command ssh-keygen to generate a new SSH key. Follow the prompts to choose a location to save the key and to set a passphrase if you want to add an extra layer of security.
2. Once the key is generated, open the file manager and navigate to the directory where the key was saved. You should see two files, one with a .pub extension (the public key) and one without (the private key).
3. Copy the contents of the public key file, typically named id_rsa.pub. You can do this by opening the file and copying the entire contents to your clipboard.
4. Go to your GitHub account in a web browser and navigate to the settings page. From there, click on the "SSH and GPG keys" tab and then click the "New SSH key" button.
5. In the "Title" field, give the key a descriptive name (e.g., "My Work Laptop") and then paste the contents of your public key into the "Key" field.
6. Save the key and go back to PyCharm. Open your project and go to the "Version Control" menu in the settings (or "Preferences" on macOS).
7. Click on the "Git" tab and locate the "SSH executable" field. Choose "Native" from the dropdown menu if it isn't already selected.
8. Under the "SSH Configuration" section, click the "Add Entry" button to add a new SSH configuration.
9. In the "Host" field, enter "github.com". In the "Port" field, enter "22". In the "Username" field, enter your GitHub username. In the "Private Key File" field, click the "..." button and navigate to the directory where your private key is stored. Select the file and click "OK".
10. Click "Test" to ensure that the configuration works. If everything is set up correctly, you should see a success message.
That's it! You should now be able to access your GitHub repositories from PyCharm using your SSH key.
Resources: https://www.youtube.com/watch?v=s6KTbytdNgs&t=86s





