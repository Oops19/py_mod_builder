#
# License: https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2021 https://github.com/Oops19
#

import argparse
import ast
import fnmatch
import re
import shutil
from typing import Set

import requests
import os
import hashlib

# GitHub, Discord and other domains with direct links work best.
# For GitHub the most recent versions will be downloaded
# For SFS URLs append "?dl/{file_name}" to the URL. Otherwise .rpartition('/') can not return a file name.
# For MEGA URLs append "/{file_name}" to the URL. Otherwise .rpartition('/') can not return a file name.
# For Nexus URLs append "#/{file_name}" to the URL. Otherwise .rpartition('/') can not return a file name.
# Nexus URLs require a manual download.
# Version updates: https://www.ea.com/de-de/games/the-sims/the-sims-4/update-notes
# __VERSION__ will be added to the README, version will be appended to the mod name.
from libraries.o19_version_handler import O19VersionHandler

sample_cfg = {
    "__VERSION__": "2021-06-29 (PC: 1.76.81.1020 / Mac: 1.76.81.1220) The Sims 4",
    "version": "2021-06-29",
    "download_folder": "TS4.ModUpdater",
    "default_mods_dir": "_cn_",
    'version_info': {
        '"sims4communitylib": "S4CL"',
    },
    "urls": {
        # Add a checksum to static URLs.
        # To overwrite the 'default_mods_dir' append "#mods_dir" with mod_dir as the name for the directory within 'Mods'
        "https://github.com/.../filename.zip": "SHA256SUM",
        "https://cdn.discordapp.com/attachments/.../filename.zip": "SHA256SUM",
        "https://www.simfileshare.net/download/.../?dl/filename.zip": "SHA256SUM",  # Add '?dl/filename.zip' to the URL
        "https://mega.nz/file//.../filename.zip": "SHA256SUM",  # Add '/filename.zip' to the URL
        "https://www.nexusmods.com/.../mods/.../filename.zip": "SHA256SUM",  # Not supported
        # Other links with static URLs are also supported. Everything behind the last '/' is considered to be the filename. Append it to the URL if needed.
        "https://....filename.zip": "SHA256SUM"
    },
    "builds": ["ColonolNutty-Patreon", "ColonolNutty-Patreon-Beta"],
    "ColonolNutty-Patreon": ["filename.v1.69.zip" ],
    "ColonolNutty-Patreon-Beta": ["filename.v1.70-beta1.zip" ],
}

tmp_directory = os.environ['tmp']

def download_file(url: str, filename: str) -> int:
    '''
    :param url:
    :param filename:
    :return: HTTP Status Code - should be 200
    '''
    file = requests.get(url, stream=True)
    if file.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(file.content)
    return file.status_code


def check_checksum(filename: str, checksum: str) -> str:
    file_checksum = ''
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            data = f.read()
            h = hashlib.sha256()
            h.update(data)
            file_checksum = h.hexdigest()

        if file_checksum == checksum:
            return file_checksum
        else:
            if checksum == '':
                print(f"For '{filename}' add '{file_checksum}' to the configuration file.")
                return file_checksum
            else:
                print(f"Deleting '{filename}' with '{file_checksum}'. Expected '{checksum}'.")
                os.remove(filename)
    return "nothing"

def get_packages(folder: str, pattern: str = '*.package') -> Set[str]:
    packages: Set[str] = set()
    for root, dirs, files in os.walk(folder):
        for filename in fnmatch.filter(files, pattern):
            package_path = str(os.path.join(root, filename))
            packages.add(package_path)
    return packages


def strip_prefix(folder: str, pattern: str = 'prefix_'):
    for root, dirs, files in os.walk(folder):
        for filename in fnmatch.filter(files, f"{pattern}*"):
            new_filename = re.sub(f"^{pattern}", "", filename)
            shutil.move(os.path.join(root, filename), os.path.join(root, new_filename))


def main():
    parser = argparse.ArgumentParser(description='Download mods.')
    parser.add_argument('--cfg', metavar='build_mods.json', type=str, nargs=1,  default='build_mods.json', help='The configuration file.')
    args = parser.parse_args()
    print(f"Using config file: {args.cfg}")
    with open(args.cfg, 'rt') as fp:
        config: dict = ast.literal_eval(fp.read())

    download_directory = os.path.join(tmp_directory, config.get('download_folder'))
    os.makedirs(download_directory, exist_ok=True)

    wrong_checksum = False
    urls = config.get('urls')
    for url, checksum in urls.items():
        url_part = url.rpartition('/')
        filename = os.path.join(download_directory, url_part[2])

        print(f"Filename: {filename}")
        check_checksum(filename, checksum)

        if not os.path.exists(filename):
            if url.startswith("https://www.nexusmods.com/"):
                print(f"Download '{url_part[2]}' manually from '{url_part[0]}'.")
            elif url.startswith(("https://mega.nz/")):
                try:
                    from mega import Mega  # Install 'mega.py', PyCharm may install 'mega'
                    print(f"Downloading '{url}'.")
                    mega = Mega()
                    m = mega.login()
                    m.download_url(url_part[0], download_directory, url_part[2])
                except Exception as e:
                    print(f"Download '{url_part[2]}' manually from '{url_part[0]}'. ({e})")
            else:
                print(f"Downloading '{url}'.")
                download_file(url, filename)

        current_checksum = check_checksum(filename, checksum)
        if current_checksum != checksum:
            print(f"Wrong checksum '{current_checksum}' for '{filename}'. Expected '{checksum}'.")
            wrong_checksum = True

    if wrong_checksum:
        exit(1)

    # All files downloaded
    o19vh = O19VersionHandler()
    release_directory = os.path.join(download_directory, 'release')
    os.makedirs(release_directory, exist_ok=True)
    shutil.rmtree(release_directory)
    for build_name in config.get('builds'):
        version_suffix = ""
        print(f"Building '{build_name}' ...")
        build_directory = os.path.join(release_directory, build_name)

        unzip_directory = os.path.join(download_directory, 'u')
        os.makedirs(unzip_directory, exist_ok=True)
        mods_directory = os.path.join(build_directory, 'Mods')
        os.makedirs(mods_directory, exist_ok=True)
        cn_scripts_directory = os.path.join(build_directory, 'Mods', config.get('default_mods_folder'))
        os.makedirs(cn_scripts_directory, exist_ok=True)


        for file in config.get(build_name):
            mod_name = file.rsplit(".", 1)[0]
            mod_documentation_directory = os.path.join(build_directory, f'mod_documentation/{mod_name}')
            os.makedirs(mod_documentation_directory, exist_ok=True)

            shutil.rmtree(unzip_directory)
            os.makedirs(unzip_directory)
            filename = os.path.join(download_directory, file)
            if filename.endswith(".package") or filename.endswith(".ts4script"):
                shutil.copy(filename, unzip_directory)
            elif filename.endswith(".zip"):
                shutil.unpack_archive(filename, unzip_directory)
            else:
                print(f"ERROR: Can't process file '{filename}' (no idea which file type)!")
            mod_data_directory = os.path.join(unzip_directory, 'mod_data')
            if os.path.exists(mod_data_directory):  # Who would want to move it to 'The Sims 4/mod_data/'?
                shutil.move(mod_data_directory, mods_directory)
            for f in get_packages(unzip_directory, '*.package'):
                shutil.move(f, cn_scripts_directory)
            for f in get_packages(unzip_directory, '*.ts4script'):
                shutil.move(f, cn_scripts_directory)
            for f in get_packages(unzip_directory, '*.config'):  # Who would want to move it to 'The Sims 4/_cn_/'?
                shutil.move(f, cn_scripts_directory)

            for f in get_packages(unzip_directory, '*.txt'):
                shutil.move(f, mod_documentation_directory)

            for f in get_packages(unzip_directory, '*.*'):
                print(f"ERROR: Skipping '{f}' (no idea where to move)!")

            strip_prefix(cn_scripts_directory, 'cn_*')

            # Add a version suffix for mods which change more often than others
            v = ''
            version_infos = config.get('version_info')
            for _file_name, _shortcut in version_infos.items():
                if file.startswith(_file_name):
                    v = _shortcut
            if v:
                version_suffix = f"{version_suffix}_{v}-v{o19vh.get_version_str(o19vh.get_version(file))}"

        # Adding the README
        __VERSION__ = config.get('__VERSION__')
        with open(os.path.join(build_directory, 'README.txt'), 'w', encoding="utf8") as outfile:
            with open(f"README.txt", encoding="utf8") as infile:
                data = infile.read()
                data = re.sub(r"__VERSION__", f"{__VERSION__}", data)
                outfile.write(data)
            outfile.write(f"\r\n\r\nIncluded mods:")
            for file in config.get(build_name):
                outfile.write(f" '{file}',")
            outfile.write(f"\r\n")
            with open(f"README.{build_name}.txt", encoding="utf8") as infile:
                outfile.write(infile.read())

        shutil.make_archive(os.path.join(release_directory, f"{build_name}_{config.get('version')}{version_suffix}"), 'zip', build_directory)


main()

