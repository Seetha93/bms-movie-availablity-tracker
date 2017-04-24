import functools
import ssl

old_init = ssl.SSLSocket.__init__

@functools.wraps(old_init)
def ubuntu_openssl_bug_965371(self, *args, **kwargs):
  kwargs['ssl_version'] = ssl.PROTOCOL_TLSv1
  old_init(self, *args, **kwargs)

ssl.SSLSocket.__init__ = ubuntu_openssl_bug_965371

#My code goes here #
import sys
import urllib2
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

def sendEmail(to, message):
    gmail_user = 'forTesting0693@gmail.com'
    gmail_pwd = 'demo1234'
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:BMS alert \n'
    print header
    msg = header + message
    smtpserver.sendmail(gmail_user, to, msg)
    print 'done!'
    smtpserver.close()

print(sys.argv[1:])
baseUrl = "https://in.bookmyshow.com"
url = baseUrl+"/"+sys.argv[3]+"/movies"

page = urllib2.urlopen(url)

soupContent = BeautifulSoup(page)

movieContainers = soupContent.findAll("div", { "class" : "card-container" })

for movieContainer in movieContainers:
  for movieDetail in movieContainer.find_all('div', {"class" : "detail"}):
      movieLanguage = movieDetail.find('li', {"class" : "__language"}).text if movieDetail.find('li', {"class" : "__language"}) is not None else ''
      # if movieLanguage is not None and movieLanguage.text.lower() == 'telugu':
      #     if movieDetail.find('a', {"class" : "__movie-name"}).text.lower() == 'baahubali 2: the conclusion':
      #         teluguAvailable = 1;
      #         moviePageLink = movieDetail.find('a').get('href')
      #         print(moviePageLink)
      #         mailContent = "Baahubali Telugu available for booking";
      #         print("Baahubali Telugu available for booking")
      # if movieLanguage is not None and movieLanguage.text.lower() == 'tamil':
      if movieDetail.find('a', {"class" : "__movie-name"}).text.lower() == sys.argv[1]:
          #tamilAvailable = 1;
          moviePageLink = movieDetail.find('a').get('href')
          mailContent = sys.argv[1]+" available for booking";
          print(sys.argv[1]+"("+movieLanguage+") available for booking")

# Looking for shows #
if 'moviePageLink' in locals() or 'moviePageLink' in globals():
  movieDetailsPage = urllib2.urlopen(baseUrl+moviePageLink)
  movieDetailsPageContent = BeautifulSoup(movieDetailsPage)

  if movieDetailsPageContent is not None:
    bookingLink = movieDetailsPageContent.find('a', {"class" : "showtimes btn _cuatro"}).get('href')

  #Bookings Page#
  bookingsPage = urllib2.urlopen(baseUrl+bookingLink+'20170428')
  bookingsPageContent = BeautifulSoup(bookingsPage)

  venueListDiv = bookingsPageContent.find('ul', {"id" : "venuelist"})
  venueList = venueListDiv.find_all('li', {"class" : "list"})
  for venue in venueList:
    listingInfo = venue.find('div', {"class" : "listing-info"})
    showTimeInfo = venue.find('div', {"class" : "body"})
    venueName = listingInfo.find('a', {"class" : "__venue-name"}).text
    availableShowTimings = showTimeInfo.find_all('a', {"class" : "__showtime-link"})
    soldOutShowTimings = showTimeInfo.find_all('div', {"class" : "_sold _soldout"})
    mailContent  = mailContent+"\n"+venueName+"\nAvailable Shows"
    print(venueName)
    print("Available Shows")
    for availableshow in availableShowTimings:
        mailContent = mailContent+availableshow.text
        print(availableshow.text)
    print("Sold Out Shows")
    for soldoutshow in soldOutShowTimings:
        print(soldoutshow.find('a').text)
if not('mailContent' in locals() or 'mailContent' in  globals()):
  mailContent = "Requested movie is not in now showing list in "+sys.argv[3]
sendEmail('rsindhu1@gmail.com', mailContent)
