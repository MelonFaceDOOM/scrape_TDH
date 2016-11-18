#NOTE: encoding error is caused by powershell encoding method. run "chcp 65001" in powershell before running this script

# Import the Selenium 2 namespace (aka "webdriver")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
				#Need to confirm: does like ID refer to a single like, or a the string of all likes in a single post?
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
		

for i in range(first_thread,92)
	#driver.find_element_by_xpath('//*[@id="inlinetopic"]/table/tbody/tr[' + str(i) + ']/td[2]/ul/li[4]/a').get_attribute('href')
	driver.find_element_by_xpath('//*[@id="inlinetopic"]/table/tbody/tr[' + str(i) + ']/td[2]/ul/li[4]/a').click()
	#
	

    


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
Go back one page if possible (to force last-post to be #90. last post of last page is unknown, so it would be tricky to check its date)
create a variable to remember the last page number
check date of last post
if date is within 2months+2days, go back a page (modify url to lower page number, unless it is already on page 1 (determine by url-name rather than finding element))
keep going back until the last post is too old.
go to the next page.
loop through all posts
keep going through pages (by modifying url) until last page is reached. 

'''