import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import shutil

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

content_template_path = "/src/content_template/"
# mounted as a docker volume
content_path = "/src/content/"
static_template_path = "/src/static_template/"
# mounted as a docker volume
static_path = "/src/static/"

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


def check_content_exists():
    if not os.listdir(content_path):
        print("Content directory is empty - copying in content_template structure")
        files = os.listdir( content_template_path )
        for file in files:
            if os.path.isdir(os.path.join(content_template_path, file)):
                print("Copying dir:", file)
                destination = shutil.copytree(
                        os.path.join(content_template_path, file), 
                        os.path.join(content_path, file)) 
            else:
                print("Copying file:", file)
                destination = shutil.copyfile(
                        os.path.join(content_template_path, file), 
                        os.path.join(content_path, file)) 


def check_static_exists():
    # Copy over the static files (css, js, img etc) if not present
    if not os.listdir(static_path):
        print("Static directory is empty - copying in static_template structure")
        files = os.listdir( static_template_path )
        for file in files:
            if os.path.isdir(os.path.join(static_template_path, file)):
                print("Copying dir:", file)
                destination = shutil.copytree(
                        os.path.join(static_template_path, file), 
                        os.path.join(static_path, file)) 
            else:
                print("Copying file:", file)
                destination = shutil.copyfile(
                        os.path.join(static_template_path, file), 
                        os.path.join(static_path, file)) 

def run_hugo():
    check_static_exists()
    check_content_exists()
    print("Content directory is not empty")
    cp = subprocess.run(["/bin/hugo"])


check_static_exists()
check_content_exists()
run_hugo()

my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, content_path, recursive=go_recursively)

my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()
