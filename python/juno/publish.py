from juno.paths import get_show_root




def next_version(publish_directory):

    all_entries = publish_directory.iterdir()
    versions_unformatted_list = []

    for i in all_entries:
        if i.is_dir():
            version = i.name
            versions_unformatted_list.append(version)


    if not versions_unformatted_list:
        return "v001"

    version_formatted_list = []

    for version in versions_unformatted_list:
        version = int(version[1:])
        version_formatted_list.append(version)

    next_num = max(version_formatted_list) + 1
    next_num = f"v{next_num:03d}"

    return next_num
