import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import stat
import shutil
import mimetypes

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(
            patterns, ignore_patterns, ignore_directories, case_sensitive)
# Embedded in hugo watcher to have at least one default site
# Currently based on the hugo-clarity theme
site_template_path = "/site_template/"
# Embedded in hugo watcher to have at least one default theme
# Currently based on the hugo-clarity theme
themes_template_path = "/themes_template/"
# mounted as a docker volume - user can replace this content as needed
# all content is removed we will replace it with the default site example
site_path = "/src"
# mounted as a docker volume
# User can drop more themes into the shared themes mount as needed
themes_path = "/themes/"

def on_created(event):
    print(f"{event.src_path} has been created!")
    run_hugo()

def on_deleted(event):
    print(f"File / path deleted: {event.src_path}!")
    run_hugo()

def on_modified(event):
    print(f"{event.src_path} has been modified")
    run_hugo()

def on_moved(event):
    print(f"File moved {event.src_path} to {event.dest_path}")
    run_hugo()


def check_site_exists():
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
        for root, dirs, files in os.walk("path"):
            for d in dirs:
                os.chmod(os.path.join(root, d), stat.S_IWOTH)
            for f in files:
                os.chmod(os.path.join(root, f), stat.S_IWOTH)

def check_themes_exists():
    # Copy over the theme files if not present
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
                # If the Env var DOMAIN is set, replace
                # any instance of example.com in the template 
                # file contents
                if os.environ.get('DOMAIN'):
                    if mimetypes.guess_type()[0] == 'text/plain':
                        file_in = open(destination, "rt")
                        contents = file_in.read()
                        contents = data.replace('example.com', os.environ.get('DOMAIN'))
                        data.close()
                        file_out = open(destination, "wt")
                        file_out.write(data)
                        file_out.close()

        for root, dirs, files in os.walk("path"):
            for d in dirs:
                os.chmod(os.path.join(root, d), stat.S_IWOTH)
            for f in files:
                os.chmod(os.path.join(root, f), stat.S_IWOTH)

def run_hugo():
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
