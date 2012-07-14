#!/usr/bin/python
# -*- coding: utf-8 -*-

import eyeD3
import ConfigParser
import re
import os


class AudioFile:
    title = None
    artists = None
    labels = None
    format = None
    name = None
    path = None
    catalog = None
    track = None
    condition = None
    tracklist = None
    track_title = None
    released = None
    country = None
    genres = None
    styles = None
    
    def __init__(self, name=None, path=None):
        self.name = name
        self.path = path
        self.track_title = None
        self.track_artists = None
        self.title = None
        self.artists = None
        self.labels = None
        self.format = None
        self.catalog = None
        self.track = None
        self.condition = None
        self.tracklist = None
        self.released = None
        self.country = None
        self.genres = None
        self.styles = None
        if re.match(".+_[ABCDEFGHIJ].?_[MVGFP]{1,2}\.mp3",name):
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
        tag.link(self.path+self.name, eyeD3.ID3_V2)
        tag.header.setVersion(eyeD3.ID3_V2_3)
        tag.setArtist(unicode(self.track_artists))
        tag.setAlbum(unicode(self.title))
        tag.setTitle(unicode(self.track_title))
        tag.removeComments()
        tag.addComment(("Label: "+unicode(self.labels)+"\n"+"Catno: "+unicode(self.catalog)+"\n"+"Format: "+unicode(self.format)+"\n"+"Track: "+unicode(self.track)+"\n"+"Released: "+unicode(self.released)+"\n"+"Country: "+unicode(self.country)+"\n"+"Genres: "+unicode(self.genres)+"\n"+"Styles: "+unicode(self.styles)+"\n").encode('latin-1','replace'))
        tag.update()
        tag.update(eyeD3.ID3_V1_1)
        
    def rename_and_move(self):
        filename = self.track_artists+' - '+self.track_title+'.mp3'
        os.rename(self.path+self.name,self.output_path_audio+filename)
        
        

