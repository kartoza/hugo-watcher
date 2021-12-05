import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import stat
import shutil
import mimetypes
import sys

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(
            patterns, ignore_patterns, ignore_directories, case_sensitive)
# Normally mounted as a docker volume
# User can drop more themes into the shared themes mount as needed
themes_path = "/themes/"
# Embedded in hugo watcher to have at least one default theme
# Currently based on the hugo-clarity theme
themes_template_path = "/themes_template/"
# Normally mounted as a docker volume - user can replace this content as needed
# all content is removed we will replace it with the default site example
site_path = "/src"

scan_lock = False

# There are three levels of overrides for the template path
# The template path provides all the initial contents for the starter site
# When the site_path is empty the site_template_path contents will
# be copied in to it to create the default starting site.
# The override priority is:
#
# 1. If the SITE_TEMPLATE_PATH env var is set, that will be used. Typically
#    you might mount this template as a docker volume so that you can 
#    provide your own template.
# 2. If the SITE_TEMPLATE_PATH is NOT set and the THEME env var is set then
#    we look in the theme dir for a folder called exampleSite and use the
#    content we find there as the basis for the site template. The naming
#    convention of exampleSite is from https://themes.gohugo.io/ which 
#    provides many nice themes.
# 3. If neither of the above are specified, we will use the exampleSite
#    folder provided in the clarity theme which is shipped with this project
#    by default insied the themes_template_path.

# Embedded in hugo watcher to have at least one default site
# Currently based on the hugo-clarity theme
site_template_path = os.path.join(
        themes_template_path,
        'hugo-clarity',
        'exampleSite')

# If the user has set a theme we override the default example site
# with the one provided in the theme
if os.environ.get('SITE_TEMPLATE_PATH'):
    site_template_path = os.environ.get('SITE_TEMPLATE_PATH')
elif os.environ.get('THEME'):
    site_template_path = os.path.join(
            themes_template_path, 
            os.environ.get('THEME'),
            'exampleSite')

def on_created(event):
    if not scan_lock:
        print(f"{event.src_path} has been created!")
        run_hugo()
    else:
        print("Scan lock enabled")

def on_deleted(event):
    if not scan_lock:
        print(f"File / path deleted: {event.src_path}!")
        run_hugo()
    else:
        print("Scan lock enabled")

def on_modified(event):
    if not scan_lock:
        print(f"{event.src_path} has been modified")
        run_hugo()
    else:
        print("Scan lock enabled")

def on_moved(event):
    if not scan_lock:
        print(f"File moved {event.src_path} to {event.dest_path}")
        run_hugo()
    else:
        print("Scan lock enabled")


def check_site_exists():
    # We take the site default content from the exampleSite directory
    # of the active theme.
    if not os.listdir(site_path):
        print("Site directory is empty - copying in site_template structure")
        files = os.listdir( site_template_path )
        for file in files:
            if os.path.isdir(os.path.join(site_template_path, file)):
                print("Copying dir:", file)
                destination = shutil.copytree(
                        os.path.join(site_template_path, file), 
                        os.path.join(site_path, file)) 
            else:
                print("Copying file:", file)
                destination = shutil.copyfile(
                        os.path.join(site_template_path, file), 
                        os.path.join(site_path, file)) 

        for root, dirs, files in os.walk(site_path):
            for directory in dirs:
                os.chmod(os.path.join(root, directory), stat.S_IWOTH)
            for file in files:
                # This breaks nginx giving a 403 on some image files
                # disabling for now
                #os.chmod(os.path.join(root, file), stat.S_IWOTH)
                # If the Env var DOMAIN is set (which should typically be the
                # case), replace any instance of example.com in the template
                # file contents
                filename, file_extension = os.path.splitext(file)
                print("Replacing example.com, example.org in :", file)
                try:
                    file_in = open(os.path.join(root, file), "rt")
                    contents = file_in.read()
                    contents = contents.replace('https://example.com', os.environ.get('DOMAIN'))
                    contents = contents.replace('https://example.org', os.environ.get('DOMAIN'))
                    contents = contents.replace('http://example.com', os.environ.get('DOMAIN'))
                    contents = contents.replace('http://example.org', os.environ.get('DOMAIN'))
                    file_in.close()
                    file_out = open(os.path.join(root, file), "wt")
                    file_out.write(contents)
                    file_out.close()
                except Exception as ex:
                    print (ex)


def check_themes_exists():
    # Copy over the theme files from the theme dir if not present
    if not os.listdir(themes_path):
        print("Themes directory is empty - copying in themes_template structure")
        files = os.listdir( themes_template_path )
        for file in files:
            if os.path.isdir(os.path.join(themes_template_path, file)):
                print("Copying dir:", file)
                destination = shutil.copytree(
                        os.path.join(themes_template_path, file), 
                        os.path.join(themes_path, file)) 
            else:
                print("Copying file:", file)
                destination = shutil.copyfile( 
                        os.path.join(themes_template_path, file), 
                        os.path.join(themes_path, file))

        for root, dirs, files in os.walk("path"):
            for d in dirs:
                os.chmod(os.path.join(root, d), stat.S_IWOTH)
            for f in files:
                os.chmod(os.path.join(root, f), stat.S_IWOTH)

def run_hugo():
    scan_lock = True
    check_site_exists()
    check_themes_exists()
    if os.environ.get('THEME'):
        print("Running hugo with theme ", os.environ.get('THEME'))
        cp = subprocess.run([
            "/bin/hugo", "--destination", "/public", 
            "--themesDir", "/themes", "--theme", os.environ.get('THEME')])
    else:
        print("Running hugo with theme hugo-clarity")
        cp = subprocess.run([
            "/bin/hugo", "--destination", "/public", 
            "--themesDir", "/themes", "--theme", "hugo-clarity"])
    scan_lock = False


check_site_exists()
check_themes_exists()
run_hugo()

my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, site_path, recursive=go_recursively)
my_observer.schedule(my_event_handler, themes_path, recursive=go_recursively)

my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()
