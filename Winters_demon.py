import sys
import json
import os
import random
import time
import subprocess
import hashlib
import importlib

from packaging import specifiers

p_count = 0
reqdepsfailed = False
easteregg_toggle = False
running_standalone = False
exit_now = False


def dependency_installer(pack_data):
    deps = pack_data.get("dependencies", {})
    if not deps:
        print("No dependencies to check.")
        return
    pip_list = "A/System42/pm_winters/pm_cache/pipcache.json"
    with open(pip_list) as file:
        pipcache_list = json.load(file)
        pipcache = {pkg["name"]: pkg["version"] for pkg in pipcache_list}
        for dep_name, dep_version_req in pack_data["dependencies"].items():
            installed_version = pipcache.get(dep_name)
            if installed_version is None:
                subprocess.run([sys.executable, "-m", "pip", "install", dep_name])
                print("DEBUG: reached end of block")

            required_specifier = SpecifierSet(dep_version_req)
            installed_ver = Version(installed_version)

            if installed_ver not in required_specifier:
                print(f"Dependency {dep_name} version {installed_version} does not meet requirement {dep_version_req}")
                # Handle upgrade, error, etc
            else:
                print(f"Dependency {dep_name} version {installed_version} meets requirement {dep_version_req}")

    return

def init_dependencies():
    marker_file = "A/System42/pm_winters/.deps_checked"
    global reqdepsfailed
    if os.path.exists(marker_file) and not reqdepsfailed:
        try:
            global requests, Version, SpecifierSet
            import requests
            from packaging.specifiers import SpecifierSet
            from packaging.version import Version
        except:
            fail_repdeps()
        return
    try:
        print("Checking if pip is alive...")
        if importlib.util.find_spec("pip") is None:
            print("ERR: Pip is missing from your python installation. Please install it to use Winters.")
            print("ERR: Winters will continue to run for debug purposes, but any attempts to install packages will fail or could cause unexpected results.")
            print("INFO: You're on your own buddy :)")
            return
        print("Checking Winters init dependencies...")
        if importlib.util.find_spec("requests") is None:
            print("Installing requests module...")
            subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        if importlib.util.find_spec("packaging") is None:
            print("Installing packaging module...")
            subprocess.run([sys.executable, "-m", "pip", "install", "packaging"], check=True)

        print("Winters init dependencies fulfilled.")
        with open(marker_file, "w") as f:
            f.write("Init Dependencies installed.")
            reqdepsfailed = False
            global requests, packaging
            import requests
            import packaging
            return

    except ImportError as e:
        print("ERR: Import error occurred while importing dependencies. Installation may have failed")
        print("ERR: Failed to satisfy dependencies for Winters. Please install packaging and requests manually.")
        print("INFO: Winters will continue to run for debug purposes, but any attempts to install packages will fail.")
        print(f"Error details: {e}")
        print(f"Return code: {e.returncode}")
        print(f"stderr: {e.stderr}")
        return

    except subprocess.CalledProcessError as e:
        print("ERR: An error occurred while installing dependencies.")
        print("INFO: Winters will continue to run for debug purposes, but any attempts to install packages will fail.")
        print(f"Error details: {e}")
        return


def register_inst_chaospack():
    print("Registering Installed Chaospack...STUB!!!!")
    return

def install_chaospack(target_name=None):
    if not target_name:
        target_name = input("Enter the name of the package to install: ").strip()
    if not target_name:
        print("Err: No package name provided.")
        return
    chaospack_downloader(target_name)
    return

def chaospack_downloader(target_name):
    cache_path = "A/System42/pm_winters/pm_cache/chaos_cache.json"
    found = False
    with open(cache_path, "r", encoding="utf-8") as f:
        chaos_data = json.load(f)
    for repo in chaos_data["repo_cache"]:
        for package in repo["packages"]:
            if package["name"] == target_name:
                print("Found it!")
                version = (package["version"])
                print("Pack URL:", package["packurl"])
                print("SHA URL:", package["sha256url"])
                try:
                    chaospack_zip = requests.get(package["packurl"]).content
                    shafile = requests.get(package["sha256url"]).text.strip()
                    dependencies = package["dependencies"]
                    pack_data = {
                        "name": target_name,
                        "packversion": version,
                        "chaospack": chaospack_zip,
                        "checksum": shafile,
                        "dependencies": dependencies,
                    }
                    print("DEBUG: Pack data:", pack_data["dependencies"])
                    checksum(pack_data)
                    #Pass that shit to checksum.
                except requests.exceptions.RequestException as e:
                    print(f"ERR: Network request failed: {str(e)}")
                    return

                except KeyError as e:
                    print(f"ERR: Missing key in package data: {str(e)}")
                    return

                except ImportError as e:
                    print(f"ERR: Missing required module: {str(e)}")
                    fail_repdeps()
                    return
                except Exception as e:
                    print(f"ERR: Unexpected error: {type(e).__name__}: {str(e)}")
                    return

                found = True
                break
        if found:
            break
    if not found:
        print("ERR: Package not found!")
        return


def list_repo():
    cache_path = "A/System42/pm_winters/pm_cache/chaos_cache.json"

    if not os.path.exists(cache_path):
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)  # Make sure the directory exists
        print("Warn:Creating folder")
        with open(cache_path, "w", encoding="utf-8") as f:
            print("Warn:Creating file")
            json.dump({"repo_cache": []}, f, indent=2)

    try:
        with open(cache_path, "r", encoding="utf-8") as file:
            data = json.load(file)  # Load the JSON file into a Python dictionary

        if not data["repo_cache"]:
            print("Err:No repository data found. Try running a cache update.")
        else:
            #TODO:THIS SHIT IS OUTDATED, USED AN OLDER JSON FILE STRUCTURE. It's not what's shipping!!!!!
            #Not sure yet if this shit reads from the cache or the source list. Haven't made up my mind.
            for repo in data["repo_cache"]:  # Loop through the list of repos
                print(f"Name: {repo['name']}")
                print(f"Repo URL: {repo['repo_url']}")
                print(f"SHA URL: {repo['repo_sha']}")
                print()
    except (json.JSONDecodeError, KeyError):
        print("Err: Cache file is malformed or missing required data.")

def update_sources():
    source_path = "A/System42/pm_winters/repo_source.json"
    cache_path = "A/System42/pm_winters/pm_cache/chaos_cache.json"
    if not os.path.exists(cache_path) or not os.path.isfile(source_path):
        print("ERR: No valid cache or source file found. Unable to continue.")
        return

    with open(source_path, "r", encoding="utf-8") as file:
        repo_sources = json.load(file)
        print(repo_sources)
        return

def checksum(pack_data):
    chaospack_zip = pack_data["chaospack"]
    sha_256 = pack_data["checksum"]
    print("DBG: SHA256 checksum is:", sha_256)

    hasher = hashlib.sha256()
    hasher.update(chaospack_zip)
    pack_checksum = hasher.hexdigest()

    if sha_256 == pack_checksum:
        print("DBG: SHA256 checksum matches.")
        dependency_installer(pack_data)
        return
    else:
        print("ERR: SHA256 checksum does not match.")
        if random.randint(1, 10) == 5 and easteregg_toggle:  # 1 in 10 chance
            print("Wow, the checksum failed. A failure, just like me!")
    return


def help():
    help_text = """
    Available commands:
    update    - Update repo sources
    info      - Lists repository info
    add       - Add a new source
    remove    - Remove a source (can take an argument)
    reset     - Regenerates all Json files (or individual json files with the arguments pip/cache/source)
    pet       - Pet the demon
    exit      - Exit the shell
    ver       - Prints Winters version
    eggtoggle - Toggle Winters Eastereggs (Enables random chance for in character dialogue)
    """
    print(help_text)
    return

def piplist_update():
    pip_list = "A/System42/pm_winters/pm_cache/pipcache.json"
    try:
        pip_jsonlist = subprocess.run([sys.executable, "-m", "pip", "list", "--format=json"], capture_output=True, text=True, check=True)
        with open(pip_list, "w", encoding="utf-8") as f:
            f.write(pip_jsonlist.stdout)
            print("INFO: Regenerating Pipcache....")
            return
    except subprocess.CalledProcessError as e:
        print("ERR: Our friend pip seems to be a bit stubborn... or dead. Possibly due to no valid PATH variable.")
        print("ERR: Can't continue. Please fix your PATH. Thanks :)")
        print(f"Error details: {e}")
        print(f"Return code: {e.returncode}")
        print(f"stderr: {e.stderr}")
    except:
        print("ERR: An unknown error occurred.")
        return
#TODO:Maybe get an alternative, a second way of checking pip packages. That was my plan, but It's so janky that I decided not to add it.


def reset_json(reset_arg=None):
    cache_path = "A/System42/pm_winters/pm_cache/chaos_cache.json"
    source_path = "A/System42/pm_winters/repo_source.json"
    reset_is_a_go = False
    if not os.path.exists(cache_path):
        print("WARN: Folder and files are missing, let me fix that.")
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as f:
            print("WARN:Creating file")
            json.dump({"repo_cache": []}, f, indent=2)
    if not os.path.exists(source_path):
        with open(source_path, "w", encoding="utf-8") as f:
            json.dump({"repo_sources": []}, f, indent=2)

    if reset_arg == "pip":
        print("INFO: resetting pipcache.json")
        piplist_update()
        return
    elif reset_arg == "source":
        print("INFO: resetting repo_source.json")
        with open(source_path, "w", encoding="utf-8") as f:
            json.dump({"repo_sources": []}, f, indent=2)
            return
    elif reset_arg == "cache":
        print("INFO: resetting chaos_cache.json")
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump({"repo_cache": []}, f, indent=2)
            return
    else:
        choice = input("Are you sure you want to regenerate your repo_source, chaos_cache and pipcache files? (Y/N): ").strip().lower()
        if not choice:
            print("Err: No input, Cancelling....")
            return
        if choice in ("yes", "y", "z", "hell yeah", "nuke it"):
            reset_is_a_go = True

        if reset_is_a_go:
            if random.randint(1, 10) == 5 and easteregg_toggle:  # 1 in 10 chance
                print("I'm not a big fan of this json thing...")
            try:
                print("INFO: Deleting Files")
                os.remove(cache_path)
                os.remove(source_path)
                print("INFO: Regenerating Chaos_cache.json and repo_source.json")
                with open(source_path, "w", encoding="utf-8") as f:
                    json.dump({"repo_sources": []}, f, indent=2)
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump({"repo_cache": []}, f, indent=2)
                piplist_update()
                print("INFO: Done.")
            except (OSError, IOError) as e:
                print(f"Err: An error occurred. I'm sorry :( {e}")
                return
        else:
            return

def enable_eastereggs():
    global easteregg_toggle
    if easteregg_toggle:
        easteregg_toggle = False
        print(f"EasterEgg Toggle: {easteregg_toggle}")
        return
    else:
        easteregg_toggle = True
        print(f"EasterEgg Toggle: {easteregg_toggle}")
        return

def chatter():
    global p_count
    if p_count > 1:
        print("Cut it out! Get your hands off of me!")
    else:
        print("Hey! Stop it! I'm a demon, not some weird cat.")
        p_count += 1

def remove_source(cpkg_name=None):
    source_path = "A/System42/pm_winters/repo_source.json"
    if not os.path.exists(source_path):
        if running_standalone:
            print("ERR: No source file! Please generate one with the add or reset command!")
        else:
            print("Please use the winters reset command! You can get more information with help winters -def !!")
        return
    if not cpkg_name:
        cpkg_name = input("Enter the package name to remove: ").strip()
    print("user tried removing:" + cpkg_name)
    if not cpkg_name:
        print("Err: No package name provided.")
        return
#TODO:DO THIS NEXT!!!!!!
####################################################


def add_source():
    source_path = "A/System42/pm_winters/repo_source.json"

        # Ensure file and directory exist
    if not os.path.exists(source_path):
        os.makedirs(os.path.dirname(source_path), exist_ok=True)
        with open(source_path, "w", encoding="utf-8") as f:
            print("INFO: Generating file...")
            json.dump({"repo_sources": []}, f, indent=2)

    try:
        with open(source_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Get user input
        user_name = input("Friendly name for repo (used for lookup): ").strip()
        repo_url = input("URL to repolist.json: ").strip()
        repo_sha = input("URL to SHA checksum file: ").strip()

        # Make new entry
        new_entry = {
            "name": user_name,
            "repo_url": repo_url,
            "repo_sha": repo_sha
        }

        # Add it to the list
        data["repo_sources"].append(new_entry)

        # Save it back
        with open(source_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        print(f"Repository '{user_name}' added successfully.")
    except (json.JSONDecodeError, KeyError):
        if running_standalone:
            print("Err: Something is fucked. Run the reset command to regenerate files.")
        else:
            print("Err: Something is fucked. Run the winters reset command!")

def winters_version():
    print("Winters package manager demon")
    print("Version 1.0 for ChaOS")
    if running_standalone:
        print("Env: Running in standalone mode!")
    else:
        print("Env: Running from ChaOS!")

def fail_repdeps():
    global reqdepsfailed
    reqdepsfailed = True
    init_dependencies()

def exit_shell():
    print("Exiting Winters debug shell... Don't go stabbing anyone...")
    time.sleep(1)
    global running_standalone, exit_now
    if not running_standalone:
        exit_now = True
        return
    else:
        exit()

def print_loaded_imports():
    top_level_imports = set()  # Use a set to avoid duplicates
    for name in sys.modules:  # Loop through all imported modules
        if '.' not in name and sys.modules[name] is not None:
            top_level_imports.add(name)  # Add only the root modules that were fully loaded

    for name in sorted(top_level_imports):  # Print them alphabetically
        print(name)
    return

# A mapping of string commands to actual functions
COMMANDS = {
    "update": update_sources,
    "info": list_repo,
    "add": add_source,
    "exit": exit_shell,
    "pet": chatter,
    "remove": remove_source,
    "reset": reset_json,
    "help": help,
    "ver": winters_version,
    "eggtoggle": enable_eastereggs,
    "debug_repdeps": fail_repdeps,
    "install": install_chaospack,
    "debug_imports": print_loaded_imports
}

def winters_shell_loop():
    init_dependencies()
    print("===================================")
    print("=Welcome to the ❄ Winters ❄ Shell=")
    print("===================================")
    print("The Weather package helper")
    print("Version 1.0")
    print("Running in debug mode")
    print("Use the help command to see a list of available commands.")
    while True:
        try:
            global exit_now
            if exit_now:
                exit_now = False
                break
            command = input("Winters> ").strip()
            if not command:
                continue

            parts = command.split()
            cmd = parts[0]
            args = parts[1:]

            if cmd in COMMANDS:
                try:
                    COMMANDS[cmd](*args)
                except TypeError as e:
                    print(f"Argument error: {e}")
                except KeyboardInterrupt:
                    print("\nUse 'exit' to quit.")
            else:
                print(f"Unknown command: {cmd}")

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")

# Only run this loop if executed directly, not if imported
if __name__ == "__main__":
    easteregg_toggle = True
    running_standalone = True
    winters_shell_loop()
