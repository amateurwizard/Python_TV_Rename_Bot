import re
import os

# Creator: Tobechukwu N. Njoku
# Last Update: 2021/07/31

regex_audio = re.compile(r'.*([2-7] [0-2][ ])')       # Using Regular expression to fix audio
regex_year = re.compile(r'.*( [1-2][0-9]{3} )')     # Using Regular expression to find the year
regex_resolutions = re.compile(r'.*([1-2][0-9]{3}[p] )')     # Using Regular expression to find the resolution
regex_episode_info = re.compile(r'.*( [s][0-9]{2}[e][0-9]{2} )', re.IGNORECASE)     # Using Regular expression to find the episode info


def tv_rename(file_name):
    renaming_history = "TV Rename Bot History.txt"
    special_characters = ("(", ")", "[", "]", ":", "_", ".", " - ", "-", "  ")
    bad_metadata = {" A ": " a ", " Of ": " of ", " And ": " and ", " The ": " the ", "X26": "x26", "X.26": "x26",
                    "H26": "x26", "H.26": "x26", "Im ": "I'm ", "St ": "St. ", "WEB DL": "Web-DL", "WEBRip": "WebRip",
                    "BluRay": "Blu-ray", "Blu ray": "Blu-ray", "eztv re": "eztv.re", "a K a": "A.K.A."}

    try:
        open(renaming_history)
    except IOError:
        print("File not accessible or doesn't exist")
    finally:
        file = open(renaming_history, "a+")
        file.write(file_name + " \n")
    file.close()

    file_name, file_extension = os.path.splitext(file_name)     # Remove and save file extension

    file_name = file_name.replace("_", " ").replace(".", " ").replace("-", " ")     # Fix based on standard torrent naming schemes

    for w in special_characters:        # Remove special characters
        file_name = file_name.replace(w, " ")

    for key, value in bad_metadata.items():     # Replace broken metadata
        file_name = file_name.replace(key, value)

    audio_found = re.search(regex_audio, file_name)     # Search for misplaced item in file name
    if audio_found:
        sound_format = audio_found.group(1).strip().replace(" ", ".")
        print("Found Sound Format: " + sound_format)
        file_name = file_name.replace(audio_found.group(1), sound_format + " ")

    resolution_found = re.search(regex_resolutions, file_name)     # Search for misplaced item in file name
    if resolution_found:
        resolution = resolution_found.group(1).strip()
        print("Found Resolution: " + resolution)
        file_name = file_name.replace(resolution_found.group(1), "[" + resolution + " ")

    while file_name[-1] == " ":     # Remove trailing whitespaces
        file_name = file_name[:-1]

    year_discovered = re.search(regex_year, file_name)      # Search for year in file name
    if year_discovered:
        year = year_discovered.group(1)
        print("Found Year: " + year.strip())
        file_name = file_name.replace(year, " ")

    episode_info_found = re.search(regex_episode_info, file_name)     # Search for misplaced item in file name
    if episode_info_found:
        episode_info = episode_info_found.group(1)
        print("Found Episode Info: " + episode_info)
        file_name = file_name.replace(episode_info, " - " + episode_info + " - ")

    file_name.replace(" - [", " ")

    file_name = file_name.replace("  ", " ")        # Double check for created double spaces
    file_name += "]" + file_extension       # Re-attach the file extension
    file_name = file_name.replace(" ]", "]").replace(" - [", " [")        # Fix bug caused by repeat uses
    print("Finished: " + file_name + "\n")
    return file_name


def tv_parsing():
    image_dir = 'TV Shows/'

    # This crawls directories, it's dangerous if used incorrectly
    for tv_show_directory, subdirectory_list, files_list in os.walk(image_dir):
        print(tv_show_directory, subdirectory_list, files_list)
        for file_name in files_list:
            print('\t%s' % file_name)       # Print the file names as a string
            print("Directory Name: " + tv_show_directory)

            print(image_dir)
            image_dir = os.path.join(image_dir, file_name)  # Create the full path to filenames
            os.rename(os.path.join(tv_show_directory, file_name), os.path.join(tv_show_directory, ''.join([str(tv_rename(file_name)), ])))

    exit()


tv_parsing()
