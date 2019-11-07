ATL-8 for reference: https://github.com/delvakwa/police_radio_to_mapping
General Assembly Data Science Immersive
Project 5: Client Project
DSI-SF-CC9: Grant Wilson, J. Hall, Gabriel Perez Prieto

Executive Summary

Problem Statement
Currently, FEMA identifies areas that require immediate attention (for search and rescue efforts) either by responding to reports and requests put directly by the public or, recently, using social media posts. This tool will utilize live police radio reports to identify hot spots representing locations of people who need immediate attention. The tool will flag neighborhoods or specific streets where the police and first-respondents were called to provide assistance related to the event.
Question
How can data analysis and processing expedite the recovery process following a natural disaster utilizing police radio reports?

Background

(GIVE CREDIT TO ATL-8 AND DESCRIBE THE USEFULNESS OF THE PROJECT, OUR NEW CONTRIBUTIONS, AND POSSIBLE FUTURE EFFORTS)



Process

## Data Description

The data used for this project is from the San Francisco City Police Dispatch, aiming to automate and decrease response times on requests through police radio.

The model was created and trained on this data with the goal that we would
eventually, given the time constraint, be able to develop and connect a live
audio streaming tool to process and map possible incidents in real time.

## Data Acquisition

Broadcastify - The world’s largest source of Public Safety, Aircraft, Rail and
Marine Radio Live Audio Streams - was used as our main data source.

With the use of BART - BroadCastify Archive Toolkit - we were able to download .mp3 audio files from the source without the need of developing a scraping tool ourselves. BART made a very manual and cumbersome processes much simpler with the use of the Selenium web scraping library.

We continue to encourage future cohorts of DSI to use this tool and therefore focus on data processing and mapping.

## Data Processing and Cleaning

The data processing and cleaning can be divided into four different steps:

- Break Audio into chunks

After downloading audio files from the selected feed archive, the first step
taken was to parse each audio file and break it down into smaller chunks. With the Pydub library we were able to analyze loudness and detect silence and those were the main indicators used to create shorter and meaningful chunks of audio.

During the audio parsing and analysis, if there were no sound emitted for more than 4 seconds in a specific file, it would immediately be cut off and
saved. To identify what was the threshold for silence in a file the average file loudness was used.

Chunks of audio with more than 6 seconds and less than 60 seconds were than converted to .WAV, as this is the required format for the following step of this work, and stored.

- Speech to Text

The next step taken was to use Google Speech to Text API to analyze and
transcribe all files so we are able to analyze it. As a parameter of the
conversion, all the street names for the city of San Francisco were provided
in order to give context to the speech to text tool.

A few files were not able to be transcribed as they were either not an actual
radio call and so those were removed from the dataset.

The average confidence level in the transcripts created was 79%.

- Natural Language Processing

Using Spacy and USAdress python libraries all transcripts were analyzed in
order to extract the addresses mentioned. By feeding the Spacy model with the street names of San Francisco the model was trained to find specific addresses, and with the use of USAdress library we were able to capture address numbers and concatenate both to come up with all the possible addresses in a transcript.

It is common to see in police radio references for addresses or nearby
streets of an incident, as well as codes for each type of incident, and so
the model was tweaked to return a list of possible addresses based on the
streets and address numbers on the transcripts.

Transcripts that did not return any street addresses were dropped from the
dataset.

- Get Latitude and Longitude

By feeding the Google Maps Geocoding API with the addresses we were able to get the latitude and longitude. Those would be later used to create a map.



Live Audio Capabilities-J

Audio Enhancement-J

Point and Frequency Mapping
Once we acquired the latitude and longitude for incident points, we were faced with the challenge of finding the best way to display these results. While the Google Maps API was easier to use, we found that using folium allowed for more creativity in mapping and better represented the data as it relates to key interests of disaster response agencies. 

To simulate the high-volume of calls to emergency services in a disaster-event, we used historic crime data to demonstrate the possibilities of the mapping portion of the project. Two maps were constructed: one to give the detail for each individual reported point, and one to show neighborhood frequency of reports.

![alt text](images/map1-1.png "Folium Cluster Map")
![alt text](images/map1-2.png "Folium Cluster Map - Zoom")

![alt text](images/map2-1.png "Folium Heatmap")
![alt text](images/map2-2.png "Folium Heatmap - Zoom")

These maps show intricate details of each dispatch call, including incident number, incident time, incident type, and the location of the incident. Each of these points is codified for urgency with colors to indicate the nature of the incident. In the example map, violent crimes are codified with red and are considered more severe than crimes like public intoxication. In a disaster-event, categories should be defined for each type of anticipated disaster to give emergency responders an idea of neighborhoods requiring the most attention.

The frequency mapping also gives key information for neighborhood-wide incidents. The heatmap gives a quick read on areas requiring assistance and its inclusion balances the need for detailed information from the Point Map with the ease of quick overview of call volume from population centers.



**Software Requirements**
spacy                  2.0.12
pandas                 0.25.1
re
collections
numpy                  1.17.2
usaddresses
requests               2.22.0
os
io
time
pydub
google-cloud           0.34.0
scipy                   1.3.1
bart
datetime
beautifulsoup4          4.8.0
folium                 0.10.0
geopandas               0.6.1
ast