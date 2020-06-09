# Google Colab Management


# Idea 
Run a command in terminal to open a shell terminal in colab.
And whatever git repo you pass or local jupyter notebook.

#Done 

#Not Done

Client script which takes in username.

Asks for ngrok api token.
Give link to https://ngrok.com/
Ask for ssh password user wants to use.

Gives setup.ipynb jupyter notebook  to put in google colab.

Then pass back grok ssh port through pmolloy.com/auto-colab.

Client then picks up this ngrok port. 
Client Keeps NGrok connection alive somehow.



Load google drive file system with auth token.
Ask user to enter google auth token in colab/client maybe?
We save the auth token in adc.json and then use it to refresh auth from now on.
After the first use the user does not have to use 
This might be able to be done over ssh or via pmolloy.com/auto-colab with with the tokenencypted with public private keys. 


From then on run Client in terminal.

It will start setup.ipynb quietly in the browser. Run a startup script for you in the shell. Then open the desired jupyter notebook in the browser. and leave a terminal shell open.





## Proper ssh Shell and automated Gdrive auth.



https://ngrok.com/

## Automated Google Drive automation:
https://stackoverflow.com/questions/57772453/login-on-colab-with-gcloud-without-service-account

## A really cool CLI interface for google colab that Akshay Ashok made:
https://towardsdatascience.com/heres-how-i-made-a-cli-tool-to-work-with-google-colab-notebooks-7678a88ca662



