General Assembly Data Science Immersive

Project 5: Client Project

DSI-SF-CC9: Grant Wilson, J. Hall, Gabriel Perez Prieto

## Problem Statement
Currently, FEMA identifies areas that require immediate attention (for search and rescue efforts) either by responding to reports and requests put directly by the public or, recently, using social media posts. This tool will utilize live police radio reports to identify hot spots representing locations of people who need immediate attention. The tool will flag neighborhoods or specific streets where the police and first-respondents were called to provide assistance related to the event.
***
## Question
How can data analysis and processing expedite the recovery process following a natural disaster utilizing police radio reports?
***
## Background
Following disaster-events, Federal, State, and Local authorities are dispatched to affected regions and are faced with decisions regarding resource allocation. Police, Fire, and EMS dispatch radio are essential indicators in identifying neighborhoods in need of assistance during a disaster.

Dispatch radio offers unique value:
- Instantaneous data acquisition
- Dispatch reflects areas where immediate resources are needed
- Inherently contain location information

The mapping of dispatch radio not only offers information about where local resources have been allocated, but incident type (gas-line rupture, downed power-lines, fire related injury) allows immediate surface-level analysis of critical infrastructure priorities following a disaster event. When pairing incident-type mapping with incident-location mapping, a fuller picture begins to emerge of the scope of assistance necessary and identifies the locations that have been hardest hit.

We are indebted to the DSI-ATL-8 team for their essential contributions to the python Broadcastify Archive Toolkit which transcribes Broadcastify archived audio: [DSI-ATL-8](https://github.com/delvakwa/police_radio_to_mapping)
***
## Data Description
The data used for this project is from the San Francisco City Police Dispatch, aiming to automate and decrease response times on requests through police radio.

The model was created and trained on this data with the goal that we would
eventually, given the time constraint, be able to develop and connect a live
audio streaming tool to process and map possible incidents in real time.
***
## Data Acquisition
Broadcastify - The world’s largest source of Public Safety, Aircraft, Rail and
Marine Radio Live Audio Streams - was used as our main data source.

With the use of BART - BroadCastify Archive Toolkit - we were able to download .mp3 audio files from the source without the need of developing a scraping tool ourselves. BART made a very manual and cumbersome processes much simpler with the use of the Selenium web scraping library.

We continue to encourage future cohorts of DSI to use this tool and therefore focus on data processing and mapping.
***
## Data Processing and Cleaning
The data processing and cleaning can be divided into four different steps:
***
### Break Audio into chunks
After downloading audio files from the selected feed archive, the first step taken was to parse each audio file and break it down into smaller chunks. With the Pydub library we were able to analyze loudness and detect silence and those were the main indicators used to create shorter and meaningful chunks of audio.

During the audio parsing and analysis, if there were no sound emitted for more than 4 seconds in a specific file, it would immediately be cut off and saved. To identify what was the threshold for silence in a file the average file loudness was used.

Chunks of audio with more than 6 seconds and less than 60 seconds were than converted to .WAV, as this is the required format for the following step of this work, and stored.
___
### Speech to Text
The next step taken was to use Google Speech to Text API to analyze and transcribe all files so we are able to analyze it. As a parameter of the conversion, all the street names for the city of San Francisco were provided in order to give context to the speech to text tool.

A few files were not able to be transcribed as they were either not an actual radio call and so those were removed from the dataset. 

The average confidence level in the transcripts created was 79%.
___
### Natural Language Processing
Using Spacy and USAdress python libraries all transcripts were analyzed to extract the addresses mentioned. By feeding the Spacy model with the street names of San Francisco the model was trained to find specific addresses, and with the use of USAdress library we were able to capture address numbers and concatenate both to come up with all the possible addresses in a transcript.

It is common to see in police radio references for addresses or nearby streets of an incident, as well as codes for each type of incident, and so the model was tweaked to return a list of possible addresses based on the streets and address numbers on the transcripts. 

Transcripts that did not return any street addresses were dropped from the dataset.
___
### Get Latitude and Longitude
By feeding the Google Maps Geocoding API with the addresses we were able to get the latitude and longitude. Those would be later used to create a map.
___
## Audio Cleaning and Analysis
### Live Audio Capabilities
The model was trained on archived recordings of scanner audio from Broadcastify. This provided a large collection for training.  In a disaster, realtime data is critical to triaging resources and assessing urgency. By incorporating a live feed we were able to accomplish realtime audio processing that would be useful in a disaster. 

We used a microphone feed in our example, which can be configured to a direct line input to a police radio or scanner, or a live stream. The live audio will print out a transcript, and then feed the transcript into the address filter and mapping functions.
___
### Audio Enhancement
The audio quality from broadcastify, and on police radio in general, is noisy and sometimes difficult to decipher.  With speech-to-text technology still in a nascent state, we looked at some of the incorrect transcripts.  Much of the audio was difficult for us to clearly hear and understand ourselves.  We wanted to give the model the best data to work with so we determined that we should clean up and improve the audio quality.

In order to improve the quality of the input audio, we passed the audio through a Dolby API.  This removed noise from background sounds and static.  It attenuated for sibilance, clarifying the harsh consonant sounds like "s", "sh", "x", "ch", "t", and "th".  The API also normalized the tone, which transforms the narrow frequency band which the police radio is constricted to, to a more natural frequency spectrum that is more in line with natural human speech.
___
## Mapping
### Point and Frequency Mapping
Once we acquired the latitude and longitude for incident points, we were faced with the challenge of finding the best way to display these results. While the Google Maps API was easier to use, we found that using Folium allowed for more creativity in mapping and better represented the data as it relates to key interests of disaster response agencies. Additionally, Folium offered maps with more intricate details of surrounding businesses, parks, and bus stops that may better inform the nature of critical infrastructure damage.

To simulate the high-volume of calls to emergency services in a disaster-event, we used historic crime data to demonstrate the possibilities of the mapping portion of the project. Two maps were constructed: one to give the detail for each individual reported point, and one to show neighborhood frequency of reports.

These maps show intricate details of each dispatch call, including incident number, incident time, incident type, and the location of the incident. Each of these points is codified for urgency with colors to indicate the nature of the incident. In the example map, violent crimes are codified with red and are considered more severe than crimes like public intoxication. 

![alt text](./images/map1-1.png "Folium Cluster Map")
<strong>Cluster Map</strong>

In a disaster-event, categories should be defined for each type of anticipated disaster to give emergency responders an idea of neighborhoods requiring the most attention.

![alt text](./images/map1-2.png "Folium Cluster Map - Zoom")
<strong>Cluster Map - Zoom</strong>

The frequency mapping also gives key information for neighborhood-wide incidents. The heatmap gives a quick read on areas requiring assistance and its inclusion balances the need for detailed information from the Point Map with the ease of quick overview of call volume from population centers.

![alt text](./images/map2-1.png "Folium Heatmap")
<strong>Heatmap</strong>



![alt text](./images/map2-2.png "Folium Heatmap - Zoom")
<strong>Heatmap - Zoom</strong>
___
**Software Requirements**
___
spacy                        2.0.12

pandas                       0.25.1

re

collections

numpy                        1.17.2

usaddresses

requests                     2.22.0

os

io

time

pydub

google-cloud                 0.34.0

scipy                         1.3.1

bart

datetime

beautifulsoup4                4.8.0

folium                       0.10.0

geopandas                     0.6.1

ast

json

logging

pickle

multiprocessing

six
