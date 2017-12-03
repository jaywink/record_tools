# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ConfigParser
import os
import re

import eyeD3


class AudioFile:
    def __init__(self, name=None, path=None):
        self.name = name
        self.path = path
        if self.path[len(self.path)-1:] != '/':
            self.path += '/'
        self.track_title = None
        self.track_artists = None
        self.title = None
        self.artists = None
        self.labels = ""
        self.format = ""
        self.catalog = None
        self.track = None
        self.condition = ""
        self.tracklist = ""
        self.released = ""
        self.country = ""
        self.genres = ""
        self.styles = ""
        self.year = None
        self.track_pos = None  # Tuple x of x style
        self.images = []
        if re.match(".+_[A-Z0-9]+_[MVGFP]{1,2}\.mp3",name):
            print "MATCH",name
            splitted = name.split('_')
            self.catalog = splitted[0]
            self.track = splitted[1]
            self.condition = splitted[2][:splitted[2].find('.')]
        else:
            self.catalog = None
            self.track = None
            self.condition = None
        self.config = ConfigParser.RawConfigParser()
        self.config.read('record_tools.properties')
        self.output_path_audio = self.config.get('Local', 'output_path_audio')

    def to_string(self):
        return self.path+self.name+' '+self.catalog+' '+self.track+' '+self.condition

    def print_tags(self):
        tag = eyeD3.Tag()
        tag.link(self.path+self.name, eyeD3.ID3_V2)
        print "Artist:",tag.getArtist()
        print "Album:",tag.getAlbum()
        print "Title:",tag.getTitle()

    def set_tags(self):
        tag = eyeD3.Tag()
        tag.link(self.path+self.name)
        tag.header.setVersion(eyeD3.ID3_DEFAULT_VERSION)
        tag.setTextEncoding(eyeD3.UTF_8_ENCODING)
        tag.setArtist(unicode(self.track_artists))
        tag.setAlbum(unicode(self.title))
        tag.setTitle(unicode(self.track_title))
        tag.setDate(self.year)
        self._set_genre(tag)
        if self.track_pos:
            tag.setTrackNum(self.track_pos)
        self._add_comments(tag)
        self._add_images(tag)
        tag.update()

    def _add_images(self, tag):
        for image in self.images:
            tag.addImage(eyeD3.ImageFrame.OTHER, image)

    def _add_comments(self, tag):
        tag.removeComments()
        comments = [
            u"Label: %s" % self.labels,
            u"Catno: %s" % self.catalog,
            u"Format: %s" % self.format,
            u"Track: %s" % self.track,
            u"Released: %s" % self.released,
            u"Country: %s" % self.country,
            u"Genres: %s" % self.genres,
            u"Styles: %s" % self.styles,
        ]
        tag.addComment(u"\n".join(comments))

    def _set_genre(self, tag):
        """Discogs styles are more accurate - take first."""
        style = self.styles.split(",")[0]
        genre = eyeD3.Genre(name=style.encode("latin-1", "replace"))
        tag.setGenre(genre)

    def rename_and_move(self):
        file_name = "%s - %s" % (self.track_artists, self.track_title)
        file_name = file_name.replace("/", " ")
        full_name = self.output_path_audio + file_name
        if os.access("%s.mp3" % full_name, os.F_OK):
            count = 1
            while os.access("%s - %s.mp3" % (full_name, count), os.F_OK):
                count += 1
            full_name = "%s - %s.mp3" % (full_name, count)
        os.rename(self.path + self.name, full_name)
