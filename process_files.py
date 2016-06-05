# -*- coding: utf-8 -*-
import ConfigParser
import os
import re
import sys
import traceback
import urllib

import discogs_client

from AudioFile import AudioFile
from TrackDB import TrackDB


found = []
catnos = {}

db = TrackDB()

config = ConfigParser.RawConfigParser()
config.read('record_tools.properties')
config.browser_command = config.get('Local', 'browser_command')
config.save_to_db = config.getboolean("DB", "save_to_db")
config.discogs_token = config.get("Discogs", "token")

discogs = discogs_client.Client(
    'RecordTools/0.5 +htts://github.com/jaywink/record_tools', user_token=config.discogs_token
)

fileTuple = os.walk(sys.argv[1])


def get_artists_string(artists):
    """Get artist names from a list of Artist objects.

    :param artists: list
    :return: unicode
    """
    found = []
    for artist in artists:
        if artist.data["name"] not in (u'&', u'vs.', u'Feat.', u'Featuring', u'+'):
            name = re.sub(r" \([0-9]*\)", "", artist.data["name"])  # Clean (1) things away
            found.append(name)
    return u' & '.join(found)


for path, subpath, filename in fileTuple:
    for name in filename:
        file = AudioFile(name, path)
        if file.catalog:
            release = None
            print file.to_string()
            if len(file.catalog) > 0:
                # Check if found before
                if file.catalog not in found:
                    # Search discogs
                    results = discogs.search(file.catalog)
                    try:
                        if results:
                            print "Found",len(results), "results"
                            key = None
                            while not release:
                                for result in results:
                                    if result.data.get("type") == "master":
                                        print "..skipping master release %s" % result.title
                                        continue
                                    key = None
                                    while key not in ['y', 's', 'q']:
                                        try:
                                            print ""
                                            print u"Discogs ID: %s" % result.data['id']
                                            print u"Discogs catno: %s" % result.data["catno"]
                                            print u"Artist: %s" % get_artists_string(result.artists)
                                            print u"Title: %s" % result.title
                                            print u"Format: %s" % u' '.join(result.data['formats'][0]['descriptions'])
                                            for track in result.tracklist:
                                                print u"%s %s" % (track.position, track.title)
                                            print ""
                                            key = raw_input(u"This release? (y=accept, enter=next, o=open, s=skip, "
                                                            u"q=quit, or input Discogs ID) ")
                                        except (KeyError, AttributeError):
                                            key = ""
                                        except KeyboardInterrupt:
                                            key = 'q'
                                        if key == 'y':
                                            release = result
                                            break
                                        elif key == "":
                                            break
                                        elif key == 's':
                                            release = None
                                            break
                                        elif key == 'q':
                                            sys.exit(0)
                                        elif key.isdigit():
                                            # discogs release ID?
                                            release = discogs.release(int(key))
                                            if release:
                                                key = 'y'
                                                break
                                            else:
                                                release = None
                                                raise Exception()
                                        elif key == 'o':
                                            os.system(config.browser_command+
                                                      ' http://www.discogs.com/release/'+str(result.data['id']))
                                            key = None
                                    if key in ['s', 'y', 'q']:
                                        break
                                if key in ['s', 'q']:
                                    break
                            if release:
                                found.append(file.catalog)
                                catnos[file.catalog] = release
                    except SystemExit:
                        sys.exit(0)
                    except:
                        traceback.print_exc()
                        print "None found!"
                        key = raw_input("Input Discogs ID or enter (%s): " % file.catalog)
                        if key.isdigit():
                            release = discogs.release(int(key))
                            if release:
                                found.append(file.catalog)
                                catnos[file.catalog] = release
                            else:
                                release = None
                else:
                    print "Already previously found!"
                    release = catnos[file.catalog]
                # Here we should have a release
                if release:
                    file.catalog = release.data["catno"]  # Replace with the one from discogs
                    file.year = release.year
                    file.artists = get_artists_string(release.artists)
                    file.labels = u", ".join([label.data["name"] for label in release.labels])
                    file.title = release.title.strip('?/*')
                    file.format = u' '.join(release.data['formats'][0]['descriptions'])
                    tracklist = []
                    for count, track in enumerate(release.tracklist, 1):
                        print u"%s - %s) %s" % (count, track.position, track.title)
                        tracklist.append(u"%s) %s" % (track.position, track.title))
                        if track.position == file.track or track.position == "B" and file.track == "AA":
                            file.track_title = track.title
                            file.track_artists = get_artists_string(track.artists)
                            if not file.track_artists:
                                file.track_artists = file.artists
                            file.track_pos = (count, len(release.tracklist))
                    file.tracklist = u'\n'.join(tracklist)
                    if "released_formatted" in release.data:
                        file.released = release.data['released_formatted']
                    if "country" in release.data:
                        file.country = release.data['country']
                    file.genres = u', '.join(release.data['genres'])
                    file.styles = u', '.join(release.data['styles'])
                    if release.images:
                        for counter, image in enumerate(release.images, 1):
                            extension = image["resource_url"].split(".")[-1]
                            image_path = "/tmp/record_tools_image_tmp_%s.%s" % (counter, extension)
                            urllib.urlretrieve(image["resource_url"], image_path)
                            file.images.append(image_path)
                    if not file.track_title:
                        print "Could not map file track info to release tracks! (%s)" % file.to_string()
                        print ""
                        track_input = raw_input("Please select track from list: ")
                        try:
                            file.track_title = release.tracklist[int(track_input)-1].title
                            file.track_artists = get_artists_string(release.tracklist[int(track_input)-1].artists)
                            if not file.track_artists:
                                file.track_artists = file.artists
                            file.track_pos = (int(track_input), len(release.tracklist))
                        except Exception:
                            print "Track selection failed, skipping this file.."
                            traceback.print_exc()
                            print release.tracklist
                    # Here we should have a track title, which is required to continue
                    if file.track_title and file.track_artists and file.name:
                        print ""
                        print "Track title:  %s" % file.track_title
                        print "Artist:       %s" % file.track_artists
                        print "TrackNo:      %s of %s" % (file.track_pos[0], file.track_pos[1])
                        key = raw_input("Confirm - s to skip, any other accept: ")
                        if key != 's':
                            if config.save_to_db:
                                db.connect()
                                db_result = db.add_release_if_none(file, release)
                                db.close()
                                if not db_result:
                                    print "Error adding to DB"
                                    sys.exit(1)
                            # Set tags
                            file.set_tags()
                            # Rename and move
                            file.rename_and_move()
                    else:
                        print "Something wrong!"
                        print vars(file)
                        sys.exit(1)
