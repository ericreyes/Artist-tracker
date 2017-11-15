import sys
from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import pprint
from bson.objectid import ObjectId

from pymongo import MongoClient
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials


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
        font.setPointSize(20)
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

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.start_button.clicked.connect(self.track_artist)
        self.save_button.clicked.connect(self.save_project)
        self.reload_button.clicked.connect(self.reload_document)

        self.graph_canvas.addWidget(self.canvas)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.query_input.setPlaceholderText(_translate("Dialog", "ArtistName/Album/Song", None))
        self.start_button.setText(_translate("Dialog", "Track \'em !", None))
        self.save_button.setText(_translate("Dialog", "Save project", None))
        self.query_input.setText(_translate("Dialog", "coldplay", None))
        self.label.setText(_translate("Dialog", "Artist name", None))
        self.plot_label.setText(_translate("Dialog", "Song popularity", None))
        self.reload_button.setText(_translate("Dialog", "Reload project", None))
        self.reload_input.setPlaceholderText(_translate("Dialog", "Project name", None))
        self.label_3.setText(_translate("Dialog", "Artist Tracker", None))


    def track_artist(self):
        artist_name = self.query_input.text()
        results = self.spotify.search(q='artist:'+ artist_name, type='artist')

        main_artist = results['artists']['items'][0]
        if main_artist:
            print ('Main artist found: {}'.format(main_artist['name']))
        else:
            print('NO ARTIST FOUND')


        related_artists = self.spotify.artist_related_artists(main_artist['id'])
        print('related artists:', '\n')
        for artist in related_artists['artists']:
            print (artist['name'], artist['popularity'], artist['followers']['total'] )

        # data = [random.random() for i in range(10)]
        # # create an axis
        # ax = self.figure.add_subplot(111)
        # # discards the old graph
        # ax.clear()
        # # plot data
        # ax.plot(data, '*-')
        # # refresh canvas
        # self.canvas.draw()

    def save_project(self):
        artist_name = self.query_input.text()
        self.query_input.setText('')
        print('saving project with name {}'.format(artist_name))
        artist_document = {'name': 'coldplay'}
        inserted_id = self.collection.insert_one(artist_document).inserted_id
        self.artists_ids.append(str(inserted_id))
        print (str(inserted_id))

    def reload_document(self):
        artist_name = self.reload_input.text()
        self.reload_input.setText('')
        print('reloading name {}'.format(artist_name))
        #Find by name
        whole_document = self.collection.find_one({'name': artist_name})
        pprint.pprint(whole_document)


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
        #self.token = util.prompt_for_user_token(self.username, client_id=self.SPOTIPY_CLIENT_ID, client_secret=self.SPOTIPY_CLIENT_SECRET, redirect_uri=self.SPOTIPY_REDIRECT_URI)

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



