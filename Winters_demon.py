import sys
import json
import os
import random
import time
import subprocess
import hashlib
import importlib
import zipfile
import io


#wegotthemvariables

#interactDDvariables
p_count = 0

reqdepsfailed = False
easteregg_toggle = False
running_standalone = False
exit_now = False

class winterspm:
    def __init__(self):
        self.depdendenciesloaded = False
        self.init_dependencies()

    def init_dependencies(self):
        init_dependencies()
        self.depdendenciesloaded = True

    def install(self, target_name=None):
        if not self.depdendenciesloaded:
            self.init_dependencies()
        install_chaospack(target_name)
        return

def chaos_extractor(pack_data):
    print("Extracting ChaosPack...")
    program_path = "A/System42/programs/" + pack_data["name"]
    try:
        with zipfile.ZipFile(io.BytesIO(pack_data["chaospack"])) as chaospack_file:
            chaospack_file.extractall(program_path)
            print("Extracted ChaosPack to:", program_path)
            register_inst_chaospack(pack_data)
            return
    except Exception as e:
        print(f"ERR: Failed to extract ChaosPack: {e}")
        return

def dependency_installer(pack_data=None, packages=None):
    standalone = packages is not None

    if standalone:
        if isinstance(packages, list):
            deps = {pkg: "" for pkg in packages}
        else:
            deps = packages
    else:
        deps = (pack_data or {}).get("dependencies") or {}

    if not deps:
        print("No dependencies to check.")
        if not standalone:
            chaos_extractor(pack_data)
        return


    to_install = []

    for name, spec in deps.items():
        name = str(name).strip()
        spec = (str(spec).strip() if spec else "")
        requirement = f"{name}{spec}" if spec else name

        show = subprocess.run([sys.executable, "-m", "pip", "show", name],capture_output=True,text=True)
        if show.returncode != 0:
            to_install.append(requirement)
            continue

        if not spec:
            continue

        installed_version = None
        for line in show.stdout.splitlines():
            if line.lower().startswith("version:"):
                installed_version = line.split(":", 1)[1].strip()
                break

        needs_update = False
        if installed_version:
            try:

                if "SpecifierSet" not in globals() or "Version" not in globals():
                    print("ERROR: Required dependency 'packaging' is missing. Aborting dependency installation.")
                    fail_repdeps()
                    print("Dependency installation cancelled.")
                    return

                needs_update = (Version(installed_version) not in SpecifierSet(spec))

            except Exception as e:
                print(f"ERROR: Version check failed ({e}). Aborting dependency installation.")
                fail_repdeps()
                print("Dependency installation cancelled.")
                return
        else:
            needs_update = True

        if needs_update:
            to_install.append(requirement)

    if not to_install:
        print("All dependencies are already satisfied.")
        if not standalone:
            chaos_extractor(pack_data)
        return

    print("The following dependencies will be installed/updated:")
    for req in to_install:
        print(f" - {req}")

    while True:
        choice = input("Proceed? (y/n): ").strip().lower()
        if choice in ("y", "n", "z", "j"):
            break
        print('Please enter "y" or "n".')

    if choice == "n":
        print("Aborted by user. No changes made.")
        return

    cmd = [sys.executable, "-m", "pip", "install"] + to_install
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("ERROR: One or more installations failed.")
        return

    print("Dependency installation complete.")
    if not standalone:
        chaos_extractor(pack_data)
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
            print("ERR: Import fail! Init dependencies failed, attempting automatic dependency repair.")
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


def register_inst_chaospack(pack_data):
    register_path = "A/System42/pm_winters/registered_packs.json"
    
    if not os.path.exists(register_path):
        os.makedirs(os.path.dirname(register_path), exist_ok=True)
        with open(register_path, "w", encoding="utf-8") as f:
            json.dump({"registered_packs": []}, f, indent=2)
            print("WARN: Registered packs list created.")
    try:
        with open(register_path, "r", encoding="utf-8") as f:
            rpack_data = json.load(f)

        new_entry = {
            "chaospack_name": pack_data["name"],
            "version": pack_data["packversion"],
            "description": pack_data["description"]
        }
        if pack_data["is_update"] or pack_data["is_reinstall"]:
            for i, pack in enumerate(rpack_data["registered_packs"]):
                if pack["chaospack_name"] == pack_data["name"]:
                    rpack_data["registered_packs"][i] = new_entry
                    print("INFO: Successfully updated/reinstalled existing chaospack.")
                    break
        else:
            rpack_data["registered_packs"].append(new_entry)
            print("INFO: Successfully installed new chaospack.")

        with open(register_path, "w", encoding="utf-8") as f:
            json.dump(rpack_data, f, indent=2)

    except KeyError as e:
        print(f"ERR: Missing required field in pack data: {e}")
    except json.JSONDecodeError:
        print("ERR: Cache file is malformed")
    except Exception as e:
        print(f"ERR: Unexpected error: {type(e).__name__}: {str(e)} Hit in Register function")
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
        for package in repo["repo"]["packages"]:
            if package["name"] == target_name:
                print("Found it!")
                found= True
                piplist_update()
                version = (package["version"])
                description = (package["description"])
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
                        "description":  description,
                        "is_update": False,
                        "is_reinstall": False,
                    }
                    print("DEBUG: Pack data:", pack_data["dependencies"])
                    cancel_upgrade = update_check(pack_data)

                    if cancel_upgrade:
                        return
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
                    print(f"ERR: Unexpected error: {type(e).__name__}: {str(e)} Hit in Chaospack Downloader function")
                    return

        if found:
            break
    if not found:
        print("ERR: Package not found!")
        return


def update_check(pack_data):
    register_path = "A/System42/pm_winters/registered_packs.json"

    if not os.path.exists(register_path) or os.path.getsize(register_path) == 0:
        checksum(pack_data)
        return

    with open(register_path, "r", encoding="utf-8") as f:
        check_packexists = json.load(f)
        for entry in check_packexists["registered_packs"]:
            if entry["chaospack_name"] == pack_data["name"]:
                print("DEBUG: Found registered pack.")

                if entry["version"] == pack_data["packversion"]:
                    pack_data["is_reinstall"] = True
                    print("INFO: Same version is already installed.")
                    prompt_reinstall = input("Would you like to reinstall the package? (Y/N): ").strip().lower()
                    if prompt_reinstall in ("yes", "y", "z", "j"):
                        checksum(pack_data)
                        return
                    else:
                        return True  # cancel_upgrade

                elif entry["version"] < pack_data["packversion"]:
                    print("DEBUG: Newer version available.")
                    pack_data["is_update"] = True
                    prompt_upgrade = input(
                        "A newer version of this package is available. Would you like to upgrade? (Y/N): ").strip().lower()
                    if prompt_upgrade in ("yes", "y", "z", "j"):
                        print(pack_data["is_update"])
                        checksum(pack_data)
                        return
                    else:
                        return True  # cancel_upgrade

        print("DEBUG: Package not registered, proceeding with install.")
        checksum(pack_data)


def search_cache(search_term=None):
    cache_path = "A/System42/pm_winters/pm_cache/chaos_cache.json"
    if not search_term:
        print("Come on, I can't do anything with nothing.")
    if not os.path.exists(cache_path):
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        print("Warn:Creating folder")
        #Is this needed? Not sure.
        with open(cache_path, "w", encoding="utf-8") as f:
            print("Warn:Creating file")
            json.dump({"repo_cache": []}, f, indent=2)

    try:
        with open(cache_path, "r", encoding="utf-8") as file:
            data = json.load(file)  # Load the JSON file into a Python dictionary
        if not data["repo_cache"]:
            print("Err:No repository data found. Try running a cache update.")
        else:
            for repo in data["repo_cache"]:
                for package in repo["repo"]["packages"]:
                    if package["name"] == search_term:
                        print(f"Found '{search_term}' in repository cache:")
                        print(f"Repository: {repo['repo']["repoinfo"]["reponame"]}")
                        print(package["name"])
                        print(package["version"])
                        print(package["description"])
                        return

        print(f"No results found for '{search_term}' in repository cache.")
        return
    except (json.JSONDecodeError, KeyError) as e:
        print("Err: Cache file is malformed or missing required data. Please reset with the reset command.")
        print(f"Details: {type(e).__name__}: {str(e)}")

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
        if choice in ("yes", "y", "z", "j", "hell yeah", "nuke it"):
            reset_is_a_go = True

        if reset_is_a_go:
            if random.randint(1, 10) == 5 and easteregg_toggle:  # 1 in 10 chance
                print("..I'm not a big fan of this json thing...")
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
    if not cpkg_name:
        print("Err: No package name provided.")
        return

    try:
        with open(source_path, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            for i, repo in enumerate(json_data["repo_sources"]):
                if cpkg_name == repo["name"]:
                    del json_data["repo_sources"][i]
                    with open(source_path, "w", encoding="utf-8") as outfile:
                        json.dump(json_data, outfile, indent=2)
                    print(f"Repository '{cpkg_name}' removed successfully.")
                    return
            print(f"Repository '{cpkg_name}' not found.")
    except (json.JSONDecodeError, KeyError):
        print("ERR: Source file is corrupted. Try using the reset command.")


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
        while True:
            user_name = input("Friendly name for repo (used for lookup): ").strip()
            
            # Check if the name is empty
            if not user_name:
                print("ERR: Repository name cannot be empty.")
                continue
                
            # Check if the name already exists
            name_exists = any(repo["name"] == user_name for repo in data["repo_sources"])
            if name_exists:
                print(f"ERR: Repository name '{user_name}' already exists. Please choose a different name.")
                continue
                
            break  # Exit the loop if the name is valid and unique


        while True:
            repo_url = input("URL to repolist.json: ").strip()
            if not repo_url:
                print("ERR: URL cannot be empty.")
                continue

            drepo_url = any(repo["repo_url"] == repo_url for repo in data["repo_sources"])
            if drepo_url:
                print(f"ERR: URL '{repo_url}' is a duplicate.")
                continue
            break

        while True:
            repo_sha = input("URL to SHA256 checksum file: ").strip()
            if not repo_sha:
                print("ERR: SHA256 cannot be empty.")
                continue
            
            drepo_sha = any(repo["repo_sha"] == repo_sha for repo in data["repo_sources"])
            if drepo_sha:
                print(f"ERR: SHA256 '{repo_sha}' is a duplicate. That can't be right.")
                continue
            break

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
    print("Version 1.0.0 for ChaOS")
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

def clear_screen():
    try:
        if os.name in ("nt", "win32"):
            os.system('cls')
            return
        elif os.name == "posix":
            os.system('clear')
            return
    except:
        print("Err: Terminal clear failed, please consider using something that is at least Windows or a Unix like.")

        pass
    # Literally the ChaOS clear function. Cut me some slack, okay?

def dd_debugcheat():
    global DD_respect
    DD_respect = 40
    print(f"Set DD respect to {DD_respect}")
    return


# A mapping of string commands to actual functions
COMMANDS = {
    "update": update_sources,
    "search": search_cache,
    "add": add_source,
    "exit": exit_shell,
    "interact": chatter,
    "remove": remove_source,
    "reset": reset_json,
    "help": help,
    "ver": winters_version,
    "eggtoggle": enable_eastereggs,
    "debug_repdeps": fail_repdeps,
    "install": install_chaospack,
    "imports": print_loaded_imports,
    "bombtest": funnypackbombfunction,
    "dd_cheat": dd_debugcheat
}

def winters_shell_loop():
    init_dependencies()
    print("===================================")
    print("=Welcome to the ❄ Winters ❄ Shell=")
    print("===================================")
    print("The ChaOS package helper")
    print("Version 1.0")
    print("Running in debug mode")
    print("Use the help command to see a list of available commands.")
    while True:
        try:
            global exit_now
            if exit_now:
                exit_now = False
                break
            command = input("Winters> ").strip().lower()
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