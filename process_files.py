#!/usr/bin/python
# -*- coding: utf-8 -*-

from AudioFile import AudioFile
from TrackDB import TrackDB
import discogs_client as discogs
import os
import sys

found = []
artists = []
tracklist = []
labels = []
track_artists = []
catnos = {}
count = 0

db = TrackDB()

discogs.user_agent = 'RecordTools/0.4 +http://basshero.org'

fileTuple = os.walk(sys.argv[1])

for dirPath,subDir,fileName in fileTuple:
    for name in fileName:
        file = AudioFile(name,dirPath)
        if file.catalog:
            release = None
            print file.to_string()
            if len(file.catalog) > 0:
                release = None
                #check if found before
                if file.catalog not in found:
                    #search discogs
                    s = discogs.Search(file.catalog)
                    #if len(s.exactresults) > 0:
                    #    print s.exactresults
                    #    db.close()
                    #    sys.exit(0)
                    try:
                        if len(s.results()) > 0:
                            print "Found",len(s.results()),"results"
                            key = ''
                            release = None
                            while key not in ['y','s','q']:
                                for result in s.results():
                                    print ""
                                    del artists[:]
                                    for artist in result.artists:
                                        artists.append(artist.data['name'])
                                    print "Discogs ID:",result.data['id']
                                    print "Artist:",', '.join(artists)
                                    print "Title:",result.title
                                    print "Format:", ' '.join(result.data['formats'][0]['descriptions'])
                                    for track in result.tracklist:
                                        print track['position'],track['title']
                                    print ""
                                    key = raw_input("This release? (y=accept, enter=next, s=skip, q=quit, or input Discogs ID) ")
                                    if key == 'y':
                                        release = result
                                        break
                                    elif key == 's':
                                        release = None
                                        break
                                    elif key == 'q':
                                        sys.exit("Quitting..")
                                    elif key.isdigit():
                                        # discogs release ID?
                                        release = discogs.Release(int(key))
                                        if release:
                                            key = 'y'
                                            break
                                        else:
                                            release = None
                                            raise Exception()
                            if release:
                                found.append(file.catalog)
                                catnos[file.catalog] = release
                    except:
                        print "None found!"
                        key = raw_input("Input Discogs ID or enter: ")
                        if key.isdigit():
                            release = discogs.Release(int(key))
                            if release:
                                found.append(file.catalog)
                                catnos[file.catalog] = release
                            else:
                                release = None
                else:
                    print "Already previously found!"
                    release = catnos[file.catalog]
                #here we should have a release
                if release:
                    del artists[:]
                    for artist in release.artists:
                        if artist not in (u'&',u'vs.','Feat.'):
                            artists.append(artist.data['name'])
                    file.artists = ', '.join(artists)
                    del labels[:]
                    for label in release.labels:
                        labels.append(label.data['name'])
                    file.labels = ', '.join(labels)
                    try:
                        file.title = release.title
                    except:
                        file.title = release.title.strip('*')
                    file.format = ' '.join(release.data['formats'][0]['descriptions'])
                    del tracklist[:]
                    for track in release.tracklist:
                        tracklist.append(track['position']+') '+track['title'])
                        if track['position'] == file.track:
                            file.track_title = track['title']
                            if len(track['artists']) > 0:
                                print track['artists']
                                del track_artists[:]
                                for artist in track['artists']:
                                    if artist not in (u'&',u'vs.','Feat.'):
                                        track_artists.append(artist.data['name'])
                                file.track_artists = ', '.join(track_artists)
                            else:
                                file.track_artists = file.artists
                    file.tracklist = '\n'.join(tracklist)
                    try:
                        file.released = release.data['released_formatted']
                    except:
                        file.released = ''
                    file.country = release.data['country']
                    file.genres = ', '.join(release.data['genres'])
                    file.styles = ', '.join(release.data['styles'])
                    if not file.track_title:
                        print "Could not map file track info to release tracks!"
                        print ""
                        for track in release.tracklist:
                            print str(release.tracklist.index(track)+1)+")",track['position'],track['title']
                        print ""
                        track_input = raw_input("Please select track from list: ")
                        try:
                            file.track_title = release.tracklist[int(track_input)-1]['title']
                            if len(release.tracklist[int(track_input)-1]['artists']) > 0:
                                del track_artists[:]
                                for artist in release.tracklist[int(track_input)-1]['artists']:
                                    if artist not in (u'&',u'vs.','Feat.', 'Featuring'):
                                        track_artists.append(artist.data['name'])
                                file.track_artists = ', '.join(track_artists)
                            else:
                                file.track_artists = file.artists
                        except Exception, e:
                            print "Track selection failed, skipping this file.."
                            print e.message
                            print release.tracklist
                    #here we should have a track title, which is required to continue
                    if file.track_title and file.track_artists and file.name:
                        #should doublecheck track name - been some errors
                        print ""
                        print "Track title: ",file.track_title
                        print "Artist:      ",file.track_artists
                        key = raw_input("Confirm - s to skip, any other accept: ")
                        if key != 's':
                            db.connect()
                            try:
                                if db.add_release_if_none(file, release):
                                    #success, continue with tagging, etc
                                    #set tags
                                    file.set_tags()
                                    #rename and move
                                    file.rename_and_move()
                            except:
                                pass
                            db.close()

