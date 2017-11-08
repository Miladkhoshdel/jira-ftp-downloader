Welcome to jira-ftp-downloader!
===================


 **jira ftp downloader** is a simple python script. this script connect to ftp hosts and get a txt file. txt file contain information about webservers, database and ftp services. the export versions from this file and import it in related table in database.

----------


Usage
-------------

StackEdit stores your documents in your browser, which means all your documents are automatically saved locally and are accessible **offline!**

>   Usage: ./manual_fetch.py [options]
>
  Options: -s, --server    hostname/ip   |   Host
           -u, --user      user          |   User
           -p, --password  password>     |   Password
           -c, --cwd       directory     |   FTP Path
           -f, --filename  filename      |   File Name

>  Example: ./manual_fetch.py -s 192.168.1.1 -u root -p 123123 -c download/files -f list.txt
