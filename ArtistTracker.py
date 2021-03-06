import sys
from PyQt4 import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pprint
from bson.objectid import ObjectId

from pymongo import MongoClient
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import numpy as np
import matplotlib.pyplot as plt
import operator
import math

import json


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

def autolabel(ax, rects, names):
    """
    Attach a text label above each bar displaying its height
    """
    for i, rect in enumerate(rects):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')
        ax.text(rect.get_x() + rect.get_width()/2., .2*height, names[i], rotation='vertical',ha='center', va='bottom', fontsize=9)
def print_dict(d):
    new = {}
    for k, v in list(d.items()):
        if isinstance(v, dict):
            v = print_dict(v)
        new[k.replace('.', '-')] = v
    return new

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1023, 750)
        self.artists_ids = []
        self.query_input = QtGui.QLineEdit(Dialog)
        self.query_input.setGeometry(QtCore.QRect(30, 70, 601, 41))
        self.query_input.setText(_fromUtf8(""))
        self.query_input.setObjectName(_fromUtf8("query_input"))
        self.start_button = QtGui.QPushButton(Dialog)
        self.start_button.setGeometry(QtCore.QRect(640, 70, 171, 41))
        self.start_button.setObjectName(_fromUtf8("start_button"))
        self.save_button = QtGui.QPushButton(Dialog)
        self.save_button.setGeometry(QtCore.QRect(810, 70, 171, 41))
        self.save_button.setObjectName(_fromUtf8("save_button"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 40, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.plot_label = QtGui.QLabel(Dialog)
        self.plot_label.setGeometry(QtCore.QRect(440, 150, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.plot_label.setFont(font)
        self.plot_label.setObjectName(_fromUtf8("plot_label"))
        self.reload_button = QtGui.QPushButton(Dialog)
        self.reload_button.setGeometry(QtCore.QRect(240, 120, 151, 31))
        self.reload_button.setObjectName(_fromUtf8("reload_button"))
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 220, 1001, 501))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.graph_canvas = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.graph_canvas.setObjectName(_fromUtf8("graph_canvas"))
        self.reload_input = QtGui.QLineEdit(Dialog)
        self.reload_input.setGeometry(QtCore.QRect(30, 120, 201, 31))
        self.reload_input.setObjectName(_fromUtf8("reload_input"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(430, 10, 171, 51))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.compare_button = QtGui.QPushButton(Dialog)
        self.compare_button.setGeometry(QtCore.QRect(640, 120, 171, 41))
        self.compare_button.setObjectName(_fromUtf8("compare_button"))

        self.outliers_button = QtGui.QPushButton(Dialog)
        self.outliers_button.setGeometry(QtCore.QRect(810, 120, 171, 41))
        self.outliers_button.setObjectName(_fromUtf8("outliers_button"))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.start_button.clicked.connect(self.track_artist)
        self.save_button.clicked.connect(self.save_project)
        self.reload_button.clicked.connect(self.reload_document)
        self.compare_button.clicked.connect(self.compare_all_artists)
        self.outliers_button.clicked.connect(self.get_outliers)
        self.graph_canvas.addWidget(self.canvas)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.query_input.setPlaceholderText(_translate("Dialog", "ArtistName/Album/Song", None))
        self.start_button.setText(_translate("Dialog", "Track \'em !", None))
        self.save_button.setText(_translate("Dialog", "Save project", None))
        self.compare_button.setText(_translate("Dialog", "Compare all artists!", None))
        self.outliers_button.setText(_translate("Dialog", "Get song outliers", None))
        self.query_input.setText(_translate("Dialog", "", None))
        self.label.setText(_translate("Dialog", "Search", None))
        self.plot_label.setText(_translate("Dialog", "Song popularity", None))
        self.reload_button.setText(_translate("Dialog", "Reload project", None))
        self.reload_input.setPlaceholderText(_translate("Dialog", "Project name", None))
        self.label_3.setText(_translate("Dialog", "Artist Tracker", None))


    def track_artist(self):
        self.artist1_dict = {}
        self.artist2_dict = {}
        artist_name = self.query_input.text()
        results = self.spotify.search(q='artist:'+ artist_name, type='artist')


        main_artist = results['artists']['items'][0]
        if main_artist:
            print ('Main artist found: {}'.format(main_artist['name']))
        else:
            print('NO ARTIST FOUND')

        # Gives back the top 10 songs

        reponse = self.spotify.artist_top_tracks(main_artist['id'])
        for i, track in enumerate(reponse['tracks']):
            self.artist1_dict[track['name']] = track['popularity']
        pprint.pprint(self.artist1_dict)


        related_artists = self.spotify.artist_related_artists(main_artist['id'])

        enemy = related_artists['artists'][0]
        for artist in related_artists['artists']:
            if(enemy['followers']['total'] < artist['followers']['total']):
                enemy = artist

        print('\n')
        print('Quick overview of Main artist and their enemy:')
        print('name - popularity - followers')
        print(main_artist['name'], main_artist['popularity'], main_artist['followers']['total'])
        print(enemy['name'], enemy['popularity'], enemy['followers']['total'])


        # Gives back the top 10 songs
        reponse = self.spotify.artist_top_tracks(enemy['id'])
        for i, track in enumerate(reponse['tracks']):
            self.artist2_dict[track['name']] = track['popularity']
        #pprint.pprint(self.artist2_dict)


        self.main_name = main_artist['name']
        self.enemy_name = enemy['name']

        self.plot(self.artist1_dict, self.artist2_dict)

    def plot(self, artist1_dict, artist2_dict, count=None, popular_dict=None):
        if (artist2_dict == None):
            print('plotting the comparison')
            self.plot_comparison(popular_dict, count)
            return

        bar_number = 10

        ind = np.arange(bar_number)  # the x locations for the groups
        width = 0.30       # the width of the bars
        self.ax = self.figure.add_subplot(111)
        self.ax.clear()
        diff = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

        sorted_dict1 = sorted(artist1_dict.items(), key=operator.itemgetter(1), reverse=True)
        sorted_dict2 = sorted(artist2_dict.items(), key=operator.itemgetter(1), reverse=True)



        values1 = [pair[1] for pair in sorted_dict1]
        values2 = [pair[1] for pair in sorted_dict2]

        names1 = [pair[0] for pair in sorted_dict1]
        names2 = [pair[0] for pair in sorted_dict2]

        rects1 = self.ax.bar(ind, values1, width, color='g', yerr=diff)
        rects2 = self.ax.bar(ind + width, values2, width, color='c', yerr=diff)
        self.ax.set_ylabel('Popularity %')
        self.ax.set_title('Artist vs Artist comparison')
        self.ax.set_xticks(ind + width / 2)
        array = ['Top1', 'Top2', 'Top3', 'Top4', 'Top5','Top6', 'Top7', 'Top8', 'Top9', 'Top10']

        self.ax.set_xticklabels(array)
        self.ax.set_xlabel('Top songs from artists')

        #Legend with both artist names
        self.ax.legend((rects1[0], rects2[0]), (self.main_name, self.enemy_name))


        autolabel(self.ax, rects1, names1)
        autolabel(self.ax, rects2, names2)
        self.canvas.draw()

    def plot_comparison(self, popular_dict, count):
        ind = np.arange(count)  # the x locations for the groups
        width = 0.30       # the width of the bars
        self.ax = self.figure.add_subplot(111)
        self.ax.clear()
        diff = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        diff = diff[:count]


        popular_dict = sorted(popular_dict.items(), key=operator.itemgetter(1), reverse=True)
        values1 = [pair[1] for pair in popular_dict]
        names1 = [pair[0] for pair in popular_dict]

        values1.pop()
        names1.pop()
        rects1 = self.ax.bar(ind, values1, width, color='g', yerr=diff)

        self.ax.set_ylabel('Popularity %')
        self.ax.set_title('Artist vs Artist comparison')
        #Todo
        self.ax.set_xticks(ind + width / 2)
        array = ['art1', 'art2', 'art3', 'art4', 'art5','art6', 'art7', 'art8', 'art9', 'art10']

        self.ax.set_xticklabels(array)
        self.ax.set_xlabel('All related artists')

        #Legend with both artist names

        autolabel(self.ax, rects1, names1)
        self.canvas.draw()


    def save_project(self):
        artist_name = self.query_input.text()
        self.query_input.setText('')
        print('saving project with name {}'.format(artist_name))

        new1 = print_dict(self.artist1_dict)
        new2 = print_dict(self.artist2_dict)

        artist_document = {'name': artist_name, 'dict1': new1, 'dict2': new2, 'main': self.main_name, 'enemy': self.enemy_name}
        inserted_id = self.collection.insert_one(artist_document).inserted_id
        print ('sucessfully saved!')
        #self.artists_ids.append(str(inserted_id))
        #print (str(inserted_id))

    def reload_document(self):
        artist_name = self.reload_input.text()
        self.reload_input.setText('')
        print('reloading name {}'.format(artist_name))

        record = self.collection.find_one({'name':artist_name})
        main_name = record['main']
        enemy_name = record['enemy']

        self.main_name = main_name
        self.enemy_name = enemy_name
        #print (record)

        self.plot(record['dict1'], record['dict2'])
        print ('sucessfully reloaded!')

    def compare_all_artists(self):
        artist_name = self.query_input.text()
        results = self.spotify.search(q='artist:'+ artist_name, type='artist')


        main_artist = results['artists']['items'][0]
        if main_artist:
            print ('Main artist found: {}'.format(main_artist['name']))
        else:
            print('NO ARTIST FOUND')

        related_artists = self.spotify.artist_related_artists(main_artist['id'])

        count = len(related_artists['artists'])
        if count < 10:
            related_list = related_artists['artists'][:count]
        else:
            related_list = related_artists['artists'][:10]
            count = 10

        popular_dict = {}
        for artist in related_list:
            popular_dict[artist['name']] = artist['popularity']
        popular_dict[main_artist['name']] = main_artist['popularity']

        self.plot(None, None, popular_dict=popular_dict, count=count)

    def get_outliers(self):
        print ('calculating outliers')
        self.artist1_dict = {}
        self.artist2_dict = {}
        song_name = self.query_input.text()
        results = self.spotify.search(q='track:'+ song_name, type='track', limit=50)


        all_songs = results['tracks']['items']


        if all_songs:
            pprint.pprint(all_songs[0])
            print('-----------------------')

        else:
            print('NO tracks FOUND')
        media = 0

        values_list = []
        for i, song in enumerate(all_songs):
            print (i, song['name'], song['popularity'], song['artists'][0]['name'])
            values_list.append(float(song['popularity']))
            media = media + float(song['popularity'])

        mean = np.mean(values_list)
        variance = (np.std(values_list))

        print ('mean: {}'.format (mean), 'variance: {}'.format (variance))



        gaussian_array = []


        def gaussian(x, mu, sig):
            return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

        for i, song in enumerate(all_songs):
            x = float(song['popularity'])

            gaus_result = gaussian(x, mean, variance)
            gaussian_array.append(gaus_result)


        print('gaussian_array', gaussian_array)
        #aussian_array [2.5638928715899847e-59, 1.1746182954073849e-12


        # Gives back the top 10 songs

        #response = self.spotify.artist_top_tracks(main_artist['id'])
        #pprint.pprint(response)
        #for i, track in enumerate(response['tracks']):
        #    self.artist1_dict[track['name']] = track['popularity']
        #pprint.pprint(self.artist1_dict)


    def setupDB(self):
        self.client = MongoClient()
        self.db = self.client['ArtistTracker']
        self.collection = self.db['tracker']
        token = 'd2e67871f01d430c8bc7408c4908579f'

        self.SPOTIPY_CLIENT_ID = '0598cd692ec64914859bd9160897908d'
        self.SPOTIPY_CLIENT_SECRET = 'd2e67871f01d430c8bc7408c4908579f'
        self.SPOTIPY_REDIRECT_URI = 'http://ericreyes.github.io/'
        self.username = 'erickilator1@gmail.com'

        self.scope = 'playlist-modify-public'


        try:
            self.client_credentials_manager = SpotifyClientCredentials(client_id=self.SPOTIPY_CLIENT_ID, client_secret=self.SPOTIPY_CLIENT_SECRET)
            self.spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        except Exception as e:
            print ('Credentials error', e)

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()

    ui.setupUi(Dialog)
    ui.setupDB()


    Dialog.show()
    sys.exit(app.exec_())



