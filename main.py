import csv
import os
import datetime
import math
import matplotlib.pyplot as plt

#change this hard-coded stuff eventually :X
directory = 'I:\Program Files (x86)\Steam\steamapps\common\FPSAimTrainer\FPSAimTrainer\stats'

listOfChallenges = []
#prepare array with dates and challenge names
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        
        if 'Tile Frenzy - Strafing' in filename:
            challengeName = filename.split(' -')[0] + filename.split(' -')[1] + filename.split(' -')[2]
        else:
            challengeName = filename.split(' -')[0]
        
        challengeDate = filename[::-1].split('-')[1][::-1].strip()
        challengeDay = challengeDate.split('.')[2]
        challengeMonth = challengeDate.split('.')[1]
        challengeYear = challengeDate.split('.')[0]
        challengeScore = 0

        with open(directory + '\\' + filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            for row in csv_reader:
                if len(row) > 0 and row[0] == 'Score:':
                    challengeScore = row[1]

        fileDictionary = { 
            'challengeScore': challengeScore,
            'challengeDateRaw': challengeDate,
            'challengeDate': datetime.date(int(challengeYear), int(challengeMonth), int(challengeDay)),
            'challengeName': challengeName,  
        }

        listOfChallenges.append(fileDictionary)

#sort
listOfChallenges.sort(key=lambda challenge: challenge['challengeDate'])

#group the array by challenge name
groupedChallenges = {}
for challenge in listOfChallenges:
    if challenge['challengeName'] not in groupedChallenges:
        groupedChallenges[challenge['challengeName']] = []
    
    groupedChallenges[challenge['challengeName']].append(challenge)

#group by challenge date
groupedChallengesByDate = {}
for challengeName in groupedChallenges:
    listOfChallengesOfSameName = groupedChallenges[challengeName]
    listOfDays = {}
    for challenge in listOfChallengesOfSameName:
        if challenge['challengeDateRaw'] not in listOfDays:
            listOfDays[challenge['challengeDateRaw']] = []
        
        listOfDays[challenge['challengeDateRaw']].append(challenge)

    groupedChallengesByDate[challengeName] = listOfDays

#extract the average score per day
averageScores = {}
for challengeName in groupedChallengesByDate:
    averageScores[challengeName] = {}
    listOfChallengesOfSameName = groupedChallengesByDate[challengeName]
    for challengeDate in listOfChallengesOfSameName:
        listOfChallengesOfSameDate = listOfChallengesOfSameName[challengeDate]
        total = 0
        for challenge in listOfChallengesOfSameDate:
            total += float(challenge['challengeScore'])
        
        averageScores[challengeName][challengeDate] = total/len(listOfChallengesOfSameDate)
        
#print to console
# for challengeName in averageScores:
#     print(challengeName, ':')
#     dateList = averageScores[challengeName]
#     for date in dateList:
#         print('\t', date, ':', dateList[date])
    
#     print('\n')

#prepare chart arrays
charts = []
for challengeName in averageScores:
    dateList = averageScores[challengeName]
    dateArray = []
    scoreArray = []
    for date in dateList:
        dateArray.append(date)
        scoreArray.append(dateList[date])
    
    charts.append({
        'challengeName': challengeName,
        'dates': dateArray,
        'scores': scoreArray
    })


print('Processed', len(listOfChallenges), 'challenges')

#create charts
xLabel = 'Date'
yLabel = 'Score'

numberOfPages = math.ceil(len(charts) / 4)

startingIndex = 0
for number in range(0, numberOfPages):
    fig, axs = plt.subplots(4, 1, constrained_layout=True)
    fig.suptitle('Kovaak scores', fontsize=16)
    currentIndex = 0
    for number in range(startingIndex, startingIndex + 4):
        if (len(charts) - 1) < number:
            break

        dates = charts[number]['dates']
        scores = charts[number]['scores']

        axs[currentIndex].plot(dates, scores)
        axs[currentIndex].set_title(charts[number]['challengeName'])
        axs[currentIndex].set_xlabel(xLabel)
        axs[currentIndex].set_ylabel(yLabel)

        if currentIndex == 3:
            break

        currentIndex += 1
    
    startingIndex += 4

plt.show()