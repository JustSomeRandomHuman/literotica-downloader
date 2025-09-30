from requests import get as requests_get
from bs4 import BeautifulSoup
from os import makedirs as os_makedirs
from os import path as os_path
from re import sub as re_sub
from time import sleep as time_sleep
from sys import exit as sys_exit

def gettext(soup): #gets the main text.
  text = soup.find('div', class_='aa_ht') #look for the div that has all the writing in it. it has the class "aa_ht".
  if text:
   text.div.unwrap() #do some shit to it.

   return text.prettify() #make it look cool and return it.
 
def getnextpage(soup): #gets the url to the next page in the story.
  try:
    nextlink = 'https://www.literotica.com' + soup.find(title="Next Page").get('href') #take the subdomain from the next page button and append to Literotica URL.
  except:
    print('Done.') 
    sys_exit(1) #if there's is no more subdomain in the next button, stop running.

  return nextlink

def getauthor(soup):
  author = (soup.find('a', class_='y_eU').get('title')).replace(' ', '_') #find the author name in the <a> element with the class "y_eU". remove spaces because why not.

  return author

#ai wrote this function vvv
def add_leading_zero_to_single_digits(text):
    """
    Adds a leading zero to single-digit numbers found within a string.
    Multi-digit numbers remain unchanged.
    """
    def replace_single_digit(match):
        return f"0{match.group(0)}"

    # Regex to find single digits not preceded or followed by another digit
    # \b ensures whole word matching for digits, preventing partial matches
    # (?<!\d) ensures no digit before
    # (?!\d) ensures no digit after
    return re_sub(r'(?<!\d)\d(?!\d)', replace_single_digit, text)

#needed for anti bot stuff vvv
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

#stuff that gets put on the top and bottom of the html file.
html_top = """
<html>
<head>
    <meta charset=utf-8>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
"""
html_bottom = """
</body>
</html>
"""

tempurl = input('url here: ') #can only be the first page of a story, and make sure there is no "?page=1" in the url.
print("")

foldername = add_leading_zero_to_single_digits((tempurl.split('/'))[-1]) #take everything after the last / in the url and use that as the folder name.

#i tried adding the release date in iso format to the start of the folder name, but unless i want to spend a lot more time on this i could only get it
#to work for stories in a series. for some reason a story's release date is only stored on the story's page unless it's in a series, so i would have to
#go to the authors page and get the story's release date from there if it wasn't in a series. i didn't want only some stories to have dates in the
#folder name so i removed that feature. 

url = tempurl + '?page=1'

i = 1
while i != 99: #increase this if the story you're downloading has over 99 pages.

  #where the magic happens vvv
  print("Reading: " + url)
  response = requests_get(url, timeout=10, headers=headers)
  soup = BeautifulSoup(response.content, 'lxml')
  body = gettext(soup)
    
  filename = add_leading_zero_to_single_digits((((url.split('/'))[-1]).replace('?page=', '_p'))) #bruh
  fullpath = os_path.join('output', getauthor(soup), foldername) #assemble the path.
  
  if not os_path.exists(fullpath):
    os_makedirs(fullpath) #make the output folder.

  with open(os_path.join(fullpath, filename) + '.html', 'w') as file:
    file.write(html_top + body + html_bottom) #bamn
    print("Output: " + os_path.abspath(os_path.join(fullpath, filename) + ".html")) #show the absolute location of the output file.
    print("")


  if i == 1:#only make the css file once, not on each loop.
    with open(os_path.join(fullpath, "styles.css"), "w") as cssfile:
      
      #edit this vvv to change the css file automatically added to each stories' folder.
      css = """
div {
  max-width: 30em;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}
      """
      cssfile.write(css)


  next_url = getnextpage(soup)
  url = next_url
  i += 1
  #time_sleep(1)


