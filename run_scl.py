import subprocess

print("About to install the lib")

subprocess.call(["apt" , 'install', "unixODBC-devel"])

print(" After the installlation process")