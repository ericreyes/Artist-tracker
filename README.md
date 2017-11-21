# Artist-tracker
A tool to analyze artists and songs popularity using Spotify's web API and Pymongo. UI was designed with pyqt4


### Steps to install
### 1 - Clone this repositorie locally.
  Clone or download the project as a local copy.
  
### 2 - Install Anaconda
Choose regular installation according to your OS
https://conda.io/docs/user-guide/install/index.html

### 3 - Install my same environment
This step is necessary so there are not broken dependencies or any missing packages. Mostly broken thinks with pyqt4 :)

Run this command:
`conda env create -f environment.yml`

### 4 Activate your environment

If you are on windows, run this command in the terminal:
`activate py35_qt4`

If you are on Linux or iOS, run this command in the terminal:
`source activate py35_qt4`

You should see py35_qt4 on the side of your terminal, meaning your environment is activated

### 5 Run the script
Now that we have all the things we need, we just run the script with python
`python ArtistTracker.py`

You should now see the window pop up and be able to play around with the Artist Tracker
