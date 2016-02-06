import os, shutil, json
import scripts.crawler as crawl

"""
	This Script tries to serve as an Autosetup for DataScience
	- gnu-sed because OSX sed is just wrong
	- Analytical Software: R, Octave
	- Python Libraries: sklearn, pandas, matplotlib,...
	- local databases: postgres, sqlite, mysql
	- programming languages: ruby
	- other utilities: sublime, osquery
""" 

def install_packages(packages, cmd):
	for package in packages:
		os.system(cmd.format(package=package))

def read_conf(file):
	f = open(file)
	output = f.read()
	f.close()
	return json.loads(output)

def copyfiles_ext(srcdir, destdir, ext):
	for name in os.listdir(srcdir):
		if name.endswith(ext):
			path = os.path.join(srcdir, name)
			if not os.path.isfile(path):
				shutil.copytree(path, destdir + name) 

def dmg_install(app_name, file_name):
	dattach = "hdiutil attach -mountpoint {appname} {filename}"
	ddetach = "hdiutil detach {appname}"
	os.system(dattach.format(appname=app_name, filename=file_name))
	copyfiles_ext(app_name, "/Applications/", ".app")
	os.system(ddetach.format(appname=app_name))	

def install_dmg_packages(packages):
	for app_name, url in packages.iteritems():
		dmg_crawl = crawl.urlcrawl(url, "dmg")
		dmg_file_url = dmg_crawl.crawl()
		if len(dmg_file_url) >= 1:
			#download the file if there is only one dmg result
			print "downloading: " + app_name
			dmg_file = crawl.urlfile(dmg_file_url[0])
			file_path = dmg_file.download("downloads/")			
			dmg_install(app_name, file_path)	
	return None

#Creates a datascience directory in home
#Makes subfolder /datasets /scripts
foldersCmd = "mkdir ~/datascience && mkdir ~/datascience/datasets && mkdir ~/datascience/scripts"
os.system(foldersCmd)

#installing homewbrew
homebrew = """/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" """
os.system(homebrew)

#Scraping and Installing DMG files
dmg_packages = read_conf("configs/dmg_packages.conf")
install_dmg_packages(dmg_packages)

#Brew Data Science Autosetup
brew_packages = read_conf("configs/brew_packages.conf")
brew_cmd = "brew install {package} --upgrade"
install_packages(brew_packages, brew_cmd)

#Brew Cask
cask_packages = read_conf("configs/cask_packages.conf")
cask_cmd = "brew cask install {package}"
install_packages(cask_packages, cask_cmd)

#Pip Data Science install
pip_packages = read_conf("configs/pip_packages.conf")
pip_cmd = "pip install {package} --upgrade"
install_packages(pip_packages, pip_cmd)

#add R dependencies?

#things I want set up
#Bashrc, vimrc

"""
TO be added
R CMD javareconf JAVA_CPPFLAGS=-I/System/Library/Frameworks/JavaVM.framework/Headers
"""
