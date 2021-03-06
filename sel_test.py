#NOTE: encoding error is caused by powershell encoding method. run "chcp 65001" in powershell before running this script

# Import the Selenium 2 namespace (aka "webdriver")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from time import strptime
import sqlite3

path = 'D:\Python\TDHbase.db'
conn = sqlite3.connect(path)
c = conn.cursor()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS LikeTable(postlink TEXT, postdate TEXT, userprofile TEXT, likerprofile TEXT, liketype TEXT)')
	
def data_entry():
	c.execute("INSERT INTO LikeTable VALUES(?, ?, ?, ?, ?);", (PostLink, PostDate, UserProfile, LikerProfile, LikeType))
	conn.commit()
	#c.close()
	#conn.close()

# Google Chrome 
driver = webdriver.Chrome('D:\Python\chromedriver\chromedriver.exe')

driver.get('http://s4.zetaboards.com/The_Daily_Happening/index/')

username = driver.find_element_by_name("uname")
password = driver.find_element_by_name("pw")

username.send_keys("3 people")
password.send_keys("Tdh123456.")
password.send_keys(Keys.RETURN)

driver.get('http://s4.zetaboards.com/The_Daily_Happening/topic/10094890/294/?x=90')

#may also be "browser.current_url"
curr_page = driver.current_url
#assumes the topic identifier is 7 characters. For example 'topic/9991030/' = 14 characters.
start = curr_page.find('topic/') + 14
end = curr_page.find('/?x=') - len(curr_page) 
page_num = curr_page_num[start:end]
prev_page = curr_url[:start] + str(int(curr_page_num) - 1) + curr_url[end:]

driver.get(prev_page)

#453 refers to the 90th post in a page
Post = '//*[@id="topic_viewer"]/tbody/tr[448]/td[2]'
LikeID = driver.find_element_by_xpath(Post + "/span/div[@class='likebg']").get_attribute('id')
PostID = LikeID[-8:]
PostDate = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[2]/span[1]').text
#if the date is either today or yesterday
if PostDate[:3] in ("yes", "tod"):
	#go back a page
elif 



###RECORD LIKES IN CURRENT PAGE
while True:
	try:
		create_table()
		for PostNumber in range(0,100):
			Post = '//*[@id="topic_viewer"]/tbody/tr[' + str(3 + 5*(PostNumber)) + ']/td[2]'
			try:
				#note that style = 'display = none;' when there is no like. No style is present when there are likes.
				Style = driver.find_element_by_xpath(Post + "/span/div[@class='likebg']").get_attribute('style')
			except:
				pass
				
			if Style == 'display = none;':
				pass
			else:
				LikeID = driver.find_element_by_xpath(Post + "/span/div[@class='likebg']").get_attribute('id')
				LikeID2 = LikeID[4: ]
				PostID = LikeID[-8:]
				
				#Check to see what icon is at the start of the like/dislike string. Consider not checking for dislike, and just assuming dislike is first if like isn't.
				try:
					if driver.find_element_by_xpath('//*[@id="' + LikeID + '"]/table/tbody/tr/td[1]/img').get_attribute("src") == 'http://z1.ifrm.com/0/1/0/p408630/like.gif':
						BeginsWLikes = True
				except:
					BeginsWLikes = False
				
				#Assume that beginning with dislikes means that there are only dislikes.
				if BeginsWLikes == False:
					#check to see if there is an expandable like-list. Click it if present. If not, check and click on expandable dislike list.
					#Expandable variable will keep track of whether or not a list has been opened.
					Expandable = False
					try:
						if driver.find_element_by_xpath('//*[@id="' + LikeID + '"]/table/tbody/tr/td[2]/a').get_attribute('onclick')[:10] == 'viewLikers':
							driver.find_element_by_xpath('//*[@id="' + LikeID + '"]/table/tbody/tr/td[2]/a').click()
							Expandable = True
					except:
						pass
					
					#Only expandable dislikes.
					if Expandable == True:
						#Grab list of dislikes
						try:
							FirstDislike = driver.find_element_by_xpath('//*[@id="likersdiv' + LikeID2 + '"]/table/tbody/tr[1]/td[1]/span[1]').text
							if FirstDislike == '- You':
								i = 2
							else:
								i = 1
							#Print a list of all likes. If the first like is "You", start with the second name. Otherwise start with the first. Loop until there are no more names.
							while True:
								try:
									LikerProfile = driver.find_element_by_xpath('//*[@id="likersdiv' + LikeID2 + '"]/table/tbody/tr[1]/td[1]/span[' + str(i) + ']/a').get_attribute('href')
									UserProfile = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[1]/a[1]').get_attribute('href')
									PostLink = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[2]/span[2]/a').get_attribute('href')
									PostDate = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[2]/span[1]').text
									LikeType = "dislike"
									data_entry()
									i = i + 1
								except:
									break
						except:
							pass
						
					#Only non-expandable dislikes.
					#need to test to make sure it can still pull a profile if "you" is the first dislike
					if Expandable == False:
						i = 1
						while True:
							try:
								LikerProfile = driver.find_element_by_xpath('//*[@id="likersdiv' + LikeID2 + '"]/table/tbody/tr/td[2]/a + [' + str(i) + ']').get_attribute('href')
								UserProfile = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[1]/a[1]').get_attribute('href')
								PostLink = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[2]/span[2]/a').get_attribute('href')
								PostDate = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[2]/span[1]').text
								LikeType = "dislike"
								data_entry()
								i = i + 1
							except:
								break
				
				#first icon is dislikes, must account for there either being only likes or dislikes, and some combination of expandable/non-expandable
				if BeginsWLikes == True:
					#Try to click on both expandable lists if they exist.
					Expandable = False
					try:
						if driver.find_element_by_xpath('//*[@id="' + LikeID + '"]/table/tbody/tr/td[2]/a').get_attribute('onclick')[:10] == 'viewLikers':
							driver.find_element_by_xpath('//*[@id="' + LikeID + '"]/table/tbody/tr/td[2]/a').click()
							Expandable = True
					except:
						try:
							if driver.find_element_by_xpath('//*[@id="' + LikeID + '"]/table/tbody/tr/td[4]/a').get_attribute('onclick')[:10] == 'viewLikers':
								driver.find_element_by_xpath('//*[@id="' + LikeID + '"]/table/tbody/tr/td[4]/a').click()
								Expandable = True
						except:
							pass
					
					#either like/dislike expandable list has been clicked.
					if Expandable == True:
						#Grab list of likes
						try:
							FirstLike = driver.find_element_by_xpath('//*[@id="likersdiv' + LikeID2 + '"]/table/tbody/tr[1]/td[1]/span[1]').text
							if FirstLike == '- You':
								i = 2
							else:
								i = 1
							#Print a list of all likes. If the first like is "You", start with the second name. Otherwise start with the first. Loop until there are no more names.
							while True:
								try:
									LikerProfile = driver.find_element_by_xpath('//*[@id="likersdiv' + LikeID2 + '"]/table/tbody/tr[1]/td[1]/span[' + str(i) + ']/a').get_attribute('href')
									UserProfile = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[1]/a[1]').get_attribute('href')
									PostLink = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[2]/span[2]/a').get_attribute('href')
									PostDate = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[2]/span[1]').text
									LikeType = "like"
									data_entry()
									i = i + 1
								except:
									break
						except:
							pass
							
						#Grab list of dislikes
						try:
							FirstDislike = driver.find_element_by_xpath('//*[@id="likersdiv' + LikeID2 + '"]/table/tbody/tr[1]/td[3]/span[1]').text
							if FirstDislike == '- You':
								i = 2
							else:
								i = 1
							#Print a list of all likes. If the first like is "You", start with the second name. Otherwise start with the first. Loop until there are no more names.
							while True:
								try:
									LikerProfile = driver.find_element_by_xpath('//*[@id="likersdiv' + LikeID2 + '"]/table/tbody/tr[1]/td[3]/span[' + str(i) + ']/a').get_attribute('href')
									UserProfile = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[1]/a[1]').get_attribute('href')
									PostLink = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[2]/span[2]/a').get_attribute('href')
									PostDate = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[2]/span[1]').text
									LikeType = "dislike"
									data_entry()
									i = i + 1
								except:
									break
						except:
							pass
				
					#NO EXPANDABLE LIKE-LIST (<3 likes, <3 dislikes)
					#Assume that a second list, if present, is the dislike list.
					if Expandable == False:
						i = 1
						while True:
							try:
								LikerProfile = driver.find_element_by_xpath('//*[@id="likersdiv' + LikeID2 + '"]/table/tbody/tr/td[2]/a + [' + str(i) + ']').get_attribute('href')
								UserProfile = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[1]/a[1]').get_attribute('href')
								PostLink = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[2]/span[2]/a').get_attribute('href')
								PostDate = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[2]/span[1]').text
								LikeType = "like"
								data_entry()
								i = i + 1
							except:
								break
						i = 1
						while True:
							try:
								LikerProfile = driver.find_element_by_xpath('//*[@id="likersdiv' + LikeID2 + '"]/table/tbody/tr/td[4]/a + [' + str(i) + ']').get_attribute('href')
								UserProfile = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[1]/a[1]').get_attribute('href')
								PostLink = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[2]/span[2]/a').get_attribute('href')
								PostDate = driver.find_element_by_xpath('//*[@id="post-' + PostID + '"]/td[2]/span[1]').text
								data_entry()
								LikeType = "dislike"
								i = i + 1
							except:
								break
	except:
		break


c.close
conn.close

'''
for i in range(0,100)
    Try 
		if driver.find_element_by_xpath('//*[@id="inlinetopic"]/table/tbody/tr[' + str(i) + ']/td[2]').text = "Title":
			first_thread = i + 1
			break
    except:
        pass
	if i = 100 then
		quit()
		
while True:

Jul 18 2016, 09:57 PM (21)
Jul 7 2016, 02:15 AM (20)
Yesterday, 1:54 AM (18)
Yesterday, 11:54 PM (19)
Today, 5:38 PM (14)
Today, 10:31 AM (15)
33 minutes ago (14)
3 minutes ago (13)
One minute ago (14)

if postdate[:9]=='Yesterday':
	if len(postdate) == 18:
		if postdate[-2:] == AM:
			Year = str(datetime.datetime.now()[:4])
			Month = str(datetime.datetime.now()[5:7]) 
			Day = str(datetime.datetime.now()[8:10]) 
			Hour = str(datetime.datetime.now()[11:13]) 
			Minute = str(datetime.datetime.now()[14:16]) 
		elif postdate[-2:] == PM:
			
	elif len(postdate) == 19:
		if postdate[-2:] == AM:
			
		elif postdate[-2:] == PM:
			
elif postdate[:5]=='Today':
	if len(postdate) == 14:
		if postdate[-2:] == AM:
			
		elif postdate[-2:] == PM:
			
	elif len(postdate) == 15:
		if postdate[-2:] == AM:
			
		elif postdate[-2:] == PM:
			
elif len(postdate) = 20:
	if postdate[-2:] == AM:
		
	elif postdate[-2:] == PM:
		
elif len(postdate) = 21:
	if postdate[-2:] == AM:
		
	elif postdate[-2:] == PM:
		
elif postdate[:3] == 'One':
	Year = str(datetime.datetime.now()[:4])
	Month = str(datetime.datetime.now()[5:7]) 
	Day = str(datetime.datetime.now()[8:10]) 
	Hour = str(datetime.datetime.now()[11:13]) 
	Minute = str(datetime.datetime.now()[14:16]) 
	Minutes_ago = 1
elif len(postdate) == 13:
	Minutes_ago = int(postdate[:1])
elif len(postdate) == 14:
	Minutes_ago = int(postdate[:2])

jan
feb
mar
apr
may
jun
jul
aug
sep
oct
nov
dec





Lastpost_month = striptime(Lastpost_date[:3], '%b').tm_mon

for i in range(first_thread,92)
	Lastpost_date = driver.find_element_by_xpath('//*[@id="inlinetopic"]/table/tbody/tr[' + str(i) + ']/td[6]/div').text
	If Lastpost_date 
	Threads = []
	Threads.append(driver.find_element_by_xpath('//*[@id="inlinetopic"]/table/tbody/tr[' + str(i) + ']/td[2]/ul/li[4]/a').get_attribute('href'))

For Thread in Threads
	driver.get(Thread)
	
	
convert postdate to consistent format (i.e. convert "yesterday" and "today" into dates)
Note that thread-link can be extracted from the post-link in the future if you would like to see which threads different users get likes in.
add ability to loop through multiple pages of a given thread
add ability to loop through all threads on the front page

First thread is currently: '//*[@id="inlinetopic"]/table/tbody/tr[7]/td[2]/a'
Changes depending on number of pinned topics. general form would be '//*[@id="inlinetopic"]/table/tbody/tr[' + PinnedCount + 3 + ']/td[2]/a'
Could determine PinnedCount by trying to get the href of '//*[@id="inlinetopic"]/table/tbody/tr[' + 1 + i + ']/td[2]/a'  - increasing i until you encounter error. the i-value that the loop will crash on is PinnedCount+2.

Last page link is href of '//*[@id="inlinetopic"]/table/tbody/tr[7]/td[2]/ul/li[4]/a'
if that is not available, that means there is only 1 page. in this case just get the href of the thread and then loop through posts in that single thread.

Most recent post in a thread is text from '//*[@id="inlinetopic"]/table/tbody/tr[7]/td[6]/div'
if we find the oldest-like, we could then check the date value of the most-recent thread against it, and stop looking through threads once you reach a thread whose newest post is too old.

Open last page of thread
create a variable to remember the last page number
Go back one page if possible (to force last-post to be #90. last post of last page is unknown, so it would be tricky to check its date)
check date of last post
if date is within 2months+2days, go back a page (modify url to lower page number, unless it is already on page 1 (determine by url-name rather than finding element))
keep going back until the last post is too old.
go to the next page.
loop through all posts
keep going through pages (by modifying url) until last page is reached. 

#PostDate = 'One minute ago'
#PostDate = 'Today, 11:34 pm'
#PostDate = 'Yesterday, 10:34 pm'
PostDate = 'Nov 8 2016, 11:03 PM'

comma_pos = PostDate.find(',')
if PostDate[:3] in ("Yes", "Tod"):
    time = PostDate[comma_pos+2:len(PostDate)-3]
    #find length. go from 2 positions after the comma to the fourth-last character to get time.
    #last 2 letters =am/pm
#Assume that no comma means that the format is either "One minute ago" or "x minutes ago"
elif comma_pos == -1:
    if len(PostDate) == 13:
        time = PostDate[:1]
    elif PostDate[:3] == "One":
        time = 1
    else:
        time = PostDate[:2]
#mmm d yyyy,
elif comma_pos == 10:
    month = PostDate[:3]
    day = PostDate[4:5]
    year = PostDate[6:10]
    time = PostDate[12:len(PostDate)-3]
#mmm dd yyyy,
elif comma_pos == 11:
    month = PostDate[:3]
    day = PostDate[4:6]
    year = PostDate[7:11]
    time = PostDate[13:len(PostDate)-3]

print(time)
print(day)
print(month)
print(year)
print(str(datetime.datetime.now().time())[:3])

'''