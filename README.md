'referee_mistake.py' is sample code that scraps data from online NBA referee reports.
It reads link urls from 'link_per_game.xlsx' and saves all correct/incorrect calls and non-calls from the each report into 'referee_mistake.xlsx'

NBA referee report is the league's assessment of officiated events that occurred in the last two minutes of last night's games that were at or within three points during any point in the last two-minutes of the fourth quarter (and overtime, where applicable). 
The plays assessed include all calls (whistles) and notable non-calls. You may find them from https://official.nba.com/2021-22-nba-officiating-last-two-minute-reports/

Environment: Python3.7 selenium 3.141.0  pandas 1.2.4
Notice: chromedriver is required for selenium. It has to match the Google Chrome version. You may download it from https://chromedriver.chromium.org/downloads
