# Record Tools

## Description

Just a little Python project to help identify, label and handle recorded audio.

Uses Discogs (https://github.com/discogs/discogs_client) to get release information. For this you need a Discogs API token.

For mp3 ID tags, eyeD3 library (http://eyed3.nicfit.net/) is used.

Filenames in source directory are in format CATNO_TRACK_CONDITION.mp3. So for example: LBL001_A_VG.mp3

Features;
1) Uses Discogs API to get release, artist and track information.
2) Asks user to confirm and choose when information is not clear.
3) (optionally) Inserts release to MySQL DB with information from Discogs
4) Sets mp3 ID tags and images, renames the files and copies them to given folder

Let me know if you find this useful (or need help using it) :)

## Usage

Once filling `record_tools.properties` with whatever is needed:

    python process_files.py <path_to_source_files>

## License

MIT
