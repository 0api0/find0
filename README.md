#Find0 A simple script that extracts the subdomain with assetfinder, then uses the httprobe tool and checks the subdomain 
if it is working or not, and finally extracts the links for each subdomain
*******************************
🔴Requirements to run the script : 
python
Install tools ( assetfinder , httprobe, waynackurl)
********************************
🔴You can develop it and add tools to extract subdomain and extract links
*********************************
🔴Outputs:
folder with the domain name
It contains a file for the subdomain, a file for the subdomain that is working , and a file for the links extracted from each subdomain that is working.
**********************************
🔴When extracting links, use greb to filter the file and extract the parameters and put them in another file to start the scan
