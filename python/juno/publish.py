from juno.paths import get_show_root
from juno.config import resolve_template, print_dict
from pathlib import Path
import shutil
from datetime import datetime
import os
import json


# next_version : given a publish directory this function will return the next file version to create. Example: if "v001" and "v002" are found then it will return "v003".
def next_version(publish_directory):

    all_entries = publish_directory.iterdir()
    versions_list = []

    for i in all_entries:
        if i.is_dir():
            version = int(i.name.removeprefix("v"))
            versions_list.append(version)

    if not versions_list:
        return "v001"

    next_num = max(versions_list) + 1
    next_num = f"v{next_num:03d}"

    return next_num


# list_publishes : given shot and department info this will return a list of existing publish versions in the shot departments "_publish" directory.
def list_publishes(show_code, sequence_code, shot_code, department):

    publish_directory = resolve_template("shot_publish_dir", show_code=show_code,sequence_code=sequence_code,shot_code=shot_code,department=department)

    if not publish_directory.exists():
        raise FileNotFoundError("Publish directory not found.")

    all_entries = publish_directory.iterdir()
    versions_list = []

    for i in all_entries:
        if i.is_dir():
            version = i.name
            versions_list.append(version)

    return versions_list


# latest_publish : given a shot and deparment info this will return the most recent publish version.
def latest_publish(show_code, sequence_code, shot_code, department):

    publish_directory = resolve_template("shot_publish_dir", show_code=show_code,sequence_code=sequence_code,shot_code=shot_code,department=department)

    if not publish_directory.exists():
        raise FileNotFoundError("Publish directory not found.")

    all_entries = publish_directory.iterdir()
    versions_list = []

    for i in all_entries:
        if i.is_dir():
            version = int(i.name.removeprefix("v"))
            versions_list.append(version)

    if not versions_list:
        return ""

    return f"v{max(versions_list):03d}"


# publish : given a source file, shot and department info this will copy the source file into the shot deparments "_publish" folder as a new version. This will set all published files to read only. Also creates metadata.json where the file is copied to.
def publish(source, show_code, sequence_code, shot_code, department, comment):

    if not Path(source).exists():
        raise FileNotFoundError(f"Source file does not exist to publish: {source}")

    publish_directory = resolve_template("shot_publish_dir", show_code=show_code,sequence_code=sequence_code,shot_code=shot_code,department=department)

    version = next_version(publish_directory)

    publish_path = (publish_directory / version)

    publish_path.mkdir(exist_ok=False)

    published_file_path = shutil.copy2(source, publish_path)

    metadata = {
        "version": version,
        "timestamp": datetime.now().isoformat(),
        "source": str(source),
        "comment": comment,
        "user": os.environ.get("USER", "Unknown")
    }

    metadata_path = resolve_template("shot_publish_metadata", show_code=show_code,sequence_code=sequence_code,shot_code=shot_code,department=department,version=version)

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)    

    Path(published_file_path).chmod(0o444) 
    metadata_path.chmod(0o444)

    return Path(published_file_path)


# get_publish_metadata : given a shot and department info and a version number this will return the metadata for a publish.
def get_publish_metadata(show_code, sequence_code, shot_code, department, version):

    metadata_path = resolve_template("shot_publish_metadata", show_code=show_code, sequence_code=sequence_code, shot_code=shot_code, department=department, version=version)

    if not metadata_path.exists():
        raise FileNotFoundError(f"Publish metadata file not found.")

    with open(metadata_path) as f:
        data = json.load(f)

    return data


