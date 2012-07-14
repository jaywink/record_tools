#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mysql
import ConfigParser
import os

class TrackDB:
    
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.read('record_tools.properties')
        self._host = self.config.get('DB', 'host')
        self._db_name = self.config.get('DB', 'db')
        self._user = self.config.get('DB', 'user')
        self._password = self.config.get('DB', 'password')
        self._vinyl_type = int(self.config.get('DB', 'type_vinyl'))
        self._cd_type = int(self.config.get('DB', 'type_cd'))
        self._picture_default_url = self.config.get('DB', 'picture_default_url')
        self._browser_command = self.config.get('Local', 'browser_command')
        
    def connect(self):
        self._conn = mysql.connect(host=self._host, db=self._db_name, user=self._user, passwd=self._password)
        self._cursor = self._conn.cursor()

    def close(self):
        self._conn.commit()
        self._cursor.close()
        self._conn.close()
        
    def get_row(self, discogs_id):
        self._cursor.execute("""SELECT * FROM for_sale
          WHERE discogs_id = %s""", (discogs_id,))
        try:
            row = self._cursor.fetchone()
            return row
        except:
            return None
            
    def get_item_id(self, discogs_id):
        self._cursor.execute("""select id from for_sale where discogs_id = %s""", (discogs_id,))
        try:
            id = self._cursor.fetchone()[0]
            return id
        except:
            return None
            
    def get_type_id(self, type_name):
        self._cursor.execute("""select id from type where description = %s""", (type_name,))
        try:
            id = self._cursor.fetchone()[0]
            return id
        except:
            return None
    
    def add(self, data):
        self._cursor.execute("""INSERT INTO for_sale (name,price,`condition`,type,link,picture,media,notes,status,discogs_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", data)
            
    def add_type(self, description):
        self._cursor.execute("""insert into type (description) values (%s)""", (description,))
            
    def link_item_type(self, item_id, type_id):
        self._cursor.execute("""insert into item_type (item_id, type_id) values (%s, %s)""", (item_id, type_id))
        
    def add_release_if_none(self, file, release):
        if not self.get_row(release.data['id']):
            print "DB: not found"
            #link
            link = 'http://www.discogs.com/release/'+str(release.data['id'])
            #picture
            try:
                picture = release.data['images'][0]['uri150']
            except:
                picture = self._picture_default_url
            #price
            os.system(self._browser_command+' http://www.discogs.com/sell/history/'+str(release.data['id']))
            price = int(raw_input("Browser has been opened to average pice list - please input price: "))
            #notes
            notes = 'Label: '+file.labels+' - '+file.catalog+'\nFormat: '+file.format+'\nReleased: '+file.released+' ('+file.country+')\nGenres: '+file.genres+'\nStyles: '+file.styles+'\n\nTracklist:\n'+file.tracklist
            add_notes = raw_input("Add an optional comment to notes part of release: ")
            if len(add_notes) > 0:
                notes += '\n\n'+add_notes
            if file.format.find('12"') > -1 or file.format.find('Vinyl') > -1:
                type = self._vinyl_type
            elif file.format.find('CD') > -1:
                type = self._cd_type
            else:
                #check from user
                while True:
                    type_raw = raw_input('Not sure about the type for: "'+file.format.encode('ascii', 'replace')+'".\ŋPlease choose 1 for VINYL and 2 for CD: ')
                    if type_raw in ('1','2'):
                        if type_raw == '1':
                            type = self._vinyl_type
                        else:
                            type = self._vinyl_cd
                        break
            data = (str(file.artists.encode('latin-1','replace')+' - '+file.title.encode('latin-1','replace')), price, file.condition, type, link, str(picture), '', notes.encode('latin-1','replace'), 1, release.data['id'])
            try:
                self.add(data)
                for style in release.data['styles']:
                    type_id = self.get_type_id(style)
                    if not type_id:
                        self.add_type(style)
                        type_id = self.get_type_id(style)
                        if not type_id:
                            raise Exception()
                    item_id = self.get_item_id(release.data['id'])
                    try:
                        self.link_item_type(item_id, type_id)
                    except Exception, ee:
                        print "Failed to add type, message: "+ee.message
                        raise Exception()
                self._conn.commit()
                return True
            except mysql.Error, me:
                print "Error %d: %s" % (me.args[0],me.args[1])
            except Exception, e:
                print "Failed to add to DB! Message: "+e.message
                self._conn.rollback()
                return False
        else:
            print "DB: found"
            return True
            
