# Author: Aaron Castellino
# Date: 12/03/2018          
# File Name: CastellinoAaron_SmashBrosYoutube_CA.py
# Description: This Program searches specified videos from Youtube for Super Smash Bros

#IMPORTANT NOTICE#
#put your own API key for this program to work on line 156

#import module for using Youtube Api
from apiclient.discovery import build 
from apiclient.errors import HttpError

#import module to deep copy 2dlists
import copy

#module for finding best url
import pafy

#module for video playing
import vlc

#module to create a GUI for the video
import wx

#module to open the  web browser
import webbrowser




def showHelp(): # defines a function which prints the instructions of how to use the program
    print('\nThis Program finds Youtube videos for specific Smash Bros. characters in their respective game.\n')
    print('Once you start this application you can choose search options to search Youtube for specific')
    print('Smash Bros Videos. You can then choose to look through the search results, Change your search settings')
    print('Or Clear History.\n If you go through search results you can choose a video and if there are more then 10')
    print('videos you will have to select them through a page system. Once a video is selected you can stream it through vlc GUI,')
    print(' or open the video in Youtube. The video you watch is recorded in a text file so ')
    print('When you want to watch a video for that character again you do not rewatch the same video.\n')
    print('You can clear you video history if you choose by selecting the Clear history option in the menus.')

def getNumber(question,lowest,highest): # defines function which asks a question and get a number within a range
    num_true = False # sets num true to False
    while num_true == False: # runs while num true to False
        numbersz = input(question)# gets the number input from user
        if numbersz.isdigit() == True: # checks if input was a number
            numbersz = int(numbersz) #converts numbersz to an integer
            if numbersz > highest or numbersz < lowest: # checks if numbersz is within the range
                print('please input a number between ' + str(lowest) + ' and ' + str(highest)) #shows to user the highest and lowest value
            else: #runs if number is accpetable
                num_true = True # ends the loop by changing variable
        else: # runs if user did not input a number
            print('please input a number') # tells user to input a number
    return numbersz #returns value of numbers

def getOption(question,array_of_options): # Asks a Question and gets The answer from list with vertical numbered menus
    print(question)
    length_list = len(array_of_options) + 1 # gets the length of list and adds 1
    for list_number in range (1,length_list): # runs for length of array but every number the counter is increased by 1
        array_number = list_number - 1 # decrease list number by 1
        print(str(list_number) + ' - ' + array_of_options[array_number]) # prints the number with a corresponding number readable to user
    array_number = length_list - 1 # decreases length list by 1 and stores it
    item_use = getNumber('Enter: ',1,array_number) # gets the number that the user wants
    array_position = item_use - 1 # decreases items use by 1 and stores it in array position
    item_use = array_of_options[array_position] # gets appropriate items and stores it
    return item_use
            
def getOptionExit(question,array_of_options): # Asks a Question and gets The answer from list with vertical numbered menus and has exit button
    print(question)
    length_list = len(array_of_options) + 1 # gets the length of list and adds 1
    for list_number in range (1,length_list): # runs for length of array but every number te counter is increased by 1
        array_number = list_number - 1 # decrease list number by 1
        print(str(list_number) + ' - ' + array_of_options[array_number]) # prints the number with a corresponding number readable to user
    print(str(length_list) + ' - Exit') # prints out the button for the user to press exit
    item_use = getNumber('Enter: ',1,length_list) # gets the number that the user wants
    if item_use != length_list: #runs if user did not input exit
        array_position = item_use - 1 # decreases items use by 1 and stores it in array position
        item_use = array_of_options[array_position] # gets appropriate items and stores it
    return item_use

def getOptionNumExit(question,array_of_options): # Asks a Question and gets The answer from list with vertical numbered menus and has exit button
    print(question)
    length_list = len(array_of_options) + 1 # gets the length of list and adds 1
    for list_number in range (1,length_list): # runs for length of array but every number te counter is increased by 1
        array_number = list_number - 1 # decrease list number by 1
        print(str(list_number) + ' - ' + array_of_options[array_number]) # prints the number with a corresponding number readable to user
    print(str(length_list) + ' - Exit') # prints out the button for the user to press exit
    item_use = getNumber('Enter: ',1,length_list) # gets the number that the user wants
    if item_use == length_list: #runs if user did not input exit
        item_use = None # gets appropriate items and stores it
    else:
        item_use -= 1
    return item_use

def getOptionNumExitMultiPage(question,array_of_options): # Asks a Question and gets The answer from list with vertical numbered menus and has exit button
    #print(array_of_options)
    page = 1
    found_option = False
    total_pages= int(len(array_of_options) / 10)
    if total_pages < len(array_of_options) / 10:
        total_pages += 1
    #print(total_pages)
    while not found_option:
        
        print('\n' + question + '  Page:' + str(page) + '/' + str(total_pages) + '\n')
        
        back_page = True
        next_page = True
        if page == 1:
            back_page = False
        elif page == total_pages:
            next_page = False
        last_item = page * 10 + 1
        first_item = last_item - 10
        if not next_page:
            remainder = (len(array_of_options) % 10)
            if remainder != 0:
                last_item = first_item + remainder
        for list_number in range (first_item,last_item):
            array_number = list_number - 1 # decrease list number by 1
            print(str(list_number) + ' - ' + array_of_options[array_number]) # prints the number with a corresponding number readable to user
        last_item -= 1
        if back_page:
            last_item += 1
            back_page_num = last_item 
            print(str(back_page_num) + ' - Page Back') # prints out the button for the user to press exit
        else:
            back_page_num = -1
        if next_page:
            last_item += 1
            next_page_num = last_item
            print(str(next_page_num) + ' - Page Next') # prints out the button for the user to press exit
        else:
            next_page_num = -1
        
        last_item += 1    
        exit_option = last_item
        print(str(exit_option) + ' - Exit ')
        option_choose = getNumber('Enter: ',first_item,last_item) # gets the number that the user wants
        
        if option_choose == back_page_num:
            page -= 1
        elif option_choose == next_page_num:
            page += 1
        elif option_choose == exit_option:
            return None
        else:
            return option_choose - 1 


class Youtube_Data(object): #Class which stores and handles connecting to youtube and all data
    def __init__(self): # Generates Data when class is initalized

        self.history = []
        
        #Specified version of Api and Api key
        self.DEVELOPER_KEY = "INSERT YOU API KEY HERE" #enter your own API KEY
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
            
    def getVideos(self):
        continue_flag = True # sets flag that user did not hit exit
        
        # gets the Game User whishes ot find videos for
        game = getOptionExit('\nWhich Smash Game Would You like videos for?', ['Super Smash Bros Ultimate','Super Smash Bros. Melee'])
        
        # If smashbros melee
        if game == 'Super Smash Bros. Melee':
            self.game = 'SSBM'
            self.characters = ['Fox','Marth','Falco','Sheik','Captain Falcon','Bowser','Jigglypuff','Luigi','Samus','Yoshi','Pikachu','Link']
            self.channel = 'UCj1J3QuIftjOq9iv_rr7Egw' #link to VGBootCamp Youtube channel
            
        # If smash bros Ultiamte
        elif game == 'Super Smash Bros Ultimate':
            self.game = 'Ultimate'
            self.characters = ['Roy','Meta Knight','Link','Wario','Shulk','Ike','Bowser','King K Rool','Ridley','Zelda','Marth','Kirby','Mario','Palutena','Ganon','Inkling']
            self.channel = 'UC_OLsb_ltM1Bo408UzjKO7Q' #link to Raw Foe Youtube channel
        else:
            continue_flag = False # if user chooses exit
            
        if continue_flag:
            self.character = getOptionExit('\nWhich Character Would You like videos for?', self.characters) #  get character choice
            if str(self.character) == str(len(self.characters) + 1) :
                continue_flag = False # if user chooses exit
        
        #get the search order fromm user
        if continue_flag:
            self.order = getOptionExit('\nHow would you like the search results ordered?', ['chronological','alphabetical','Highest rating','Highest view count'])
            if self.order == 'chronological':
                self.order = 'date'
            elif self.order == 'alphabetical':
                self.order = 'title'
            elif self.order == 'Highest rating':
                self.order = 'rating'
            elif self.order == 'Highest view count':
                self.order = 'viewCount' 
            else:
                continue_flag = False # if user hits exit
                
                
        if continue_flag:
            self.search_terms = [self.game,50,self.channel,self.order] #puts the search terms into list
            try:
                self.getFileHistory() # try reading from the file
            except BaseException:
                self.writeFileHistory() # create a file if this is not possible
                self.getFileHistory()
        if continue_flag:
            try:
                print('\nLoading...\n') # print message as youtube search takes a while

                # Gets the Videos and puts them in a list
                self.youtube_search()
                self.character_vidfinder(self.videos)
                self.hide_oldvids()
                
            except HttpError: # if youtube does now work
                print("An HTTP error occurred" )
                continue_flag = False
        return continue_flag
        
        
    def youtube_search(self): # searches the Youtube Api for videos
        
        self.youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self.DEVELOPER_KEY) # builds the Youtube API
        
        #get results from the search request
        self.search_request = self.youtube.search().list( q= self.search_terms[0], part="id,snippet", maxResults=self.search_terms[1], channelId= self.search_terms[2], order = self.search_terms[3], type = 'video')

        #Create lists to store the data
        self.video_title = []
        self.video_id = []


        while self.search_request != None: # while there is something to search
            self.search_response = self.search_request.execute() # execute the search object
            
            #Check sear result for items
            for self.search_result in self.search_response.get("items", []):
                #if the item is a video
                if self.search_result["id"]["kind"] == "youtube#video":
                    # add the videos title and url to a list
                    self.video_title.append(self.search_result["snippet"]["title"])
                    self.video_id.append(self.search_result["id"]["videoId"])
            
            #get the next page of search request
            self.search_request = self.youtube.search().list_next(self.search_request,self.search_response)

        # build a 2d array of the values           
        self.videos = [self.video_title,self.video_id]
        
    def youtube_video_info(self,id_key): # Displays information of the video
        
        self.search_request = self.youtube.videos().list(part = 'snippet',id = id_key).execute() # executes a search requiest for the given video id
        self.search_result = self.search_request.get("items", []) #gets the items from the list

        try: 
            #prints various data stored in search result
            print('\nTitle: ' + self.search_result[0]["snippet"]["title"]) # prints the title from the data
            print('Date Published: ' + self.search_result[0]['snippet']['publishedAt'][0:10]) # prints the date from data
            print('Channel: ' + self.search_result[0]['snippet']['channelTitle'])
            print('Description: ' + self.search_result[0]['snippet']['description'] + '\n')
        except BaseException:
            pass #certain characters in description may be unable to print
        
        
    def display_data(self,dataset): # Display the video title and url for the youtube videos
        for x in range (0,len(dataset[0]) - 1):
            print(dataset[0][x] + 'url: https://www.youtube.com/watch?v=' + dataset[1][x])

    def character_vidfinder (self,dataset): # find the character specific videos
        #create arrays to hold the data
        self.character_vidtitle = [] 
        self.character_vidid = []
        
        #check all elements of the data set
        for x in range (0,len(dataset[0]) - 1):
            if dataset[0][x].rfind(self.character) != -1 : # if the characters name is in the title of the video
                # add the title and url to theirs array's
                self.character_vidtitle.append(dataset[0][x]) 
                self.character_vidid.append(dataset[1][x])
                
        #build a 2d array for the new data
        self.character_vids = [self.character_vidtitle,self.character_vidid]
      
    def hide_oldvids(self): # find the character specific videos
        if not self.history == []: # if history is not empty
            self.character_vids_2 = copy.deepcopy(self.character_vids) #create a copy of the videos
            for x in range (len(self.character_vids_2[0]) -1,-1,-1): # runs for each item in the array from top to bottom
                if self.historycheck(self.character_vids_2[0][x],len(self.history) - 1) == True:
                    del(self.character_vids[0][x]) # delete the video title
                    del(self.character_vids[1][x])# delete the video url
                
    def historycheck(self,title,counter):
        if title == self.history[counter]:
            return True
        elif counter > 0:
            self.historycheck(title , counter - 1)
        else:
            return False
    
    def getFileHistory(self): # Gets the History data from the file
        with open('CastellinoAaron_History.txt', 'r',encoding='UTF-8') as f:
            self.history = f.read().splitlines() #gets the data from file
        self.history = list(set(self.history))# stores data
    
    def writeFileHistory(self): # Writes the History Data to a text file
        with open('CastellinoAaron_History.txt', 'w',encoding='UTF-8') as f:
            for x in range (len(self.history) -1,-1,-1 ):
                try:
                    f.write(self.history[x])#adds data to file
                    f.write('\n') # adds new line
                except BaseException:
                    print('The video ' + self.history[x] + 'could not be encoded to the history file\n due to the special characters it contains')
                    del(self.history[x])

    def clearFileHistory(self): # clears the file history
        with open('CastellinoAaron_History.txt', 'w',encoding='UTF-8') as f: #opens the file to write
            pass


class YoutubePlayer(wx.Frame):
    def __init__(self, title,url):
        wx.Frame.__init__(self, None, -1, title,pos=wx.DefaultPosition, size=(800, 600))

        #Create a box for the videos
        self.videobox = wx.Panel(self, -1)
        self.videobox.SetBackgroundColour(wx.BLACK)

        # Create Another Box for the controlbox
        controlbox = wx.Panel(self, -1 )
        
        #create a slider for the time and volume
        self.timeslider = wx.Slider(controlbox, -1, 0, 0, 1000)
        self.timeslider.SetRange(0, 1000)
        self.volume_slide = wx.Slider(controlbox, -1, 0, 0, 100, size=(100, -1))
        
        #Create buttons for the controls
        pause_button  = wx.Button(controlbox, label="Pause")
        play_button   = wx.Button(controlbox, label="Play")
        stop_button   = wx.Button(controlbox, label="Stop")
        volume_button = wx.Button(controlbox, label="Mute")
        
        
        #create a timer
        self.timer = wx.Timer(self)

        # Bind the Events for the Controls
        self.Bind(wx.EVT_BUTTON, self.OnPlay, play_button)
        self.Bind(wx.EVT_BUTTON, self.OnPause, pause_button)
        self.Bind(wx.EVT_BUTTON, self.OnStop, stop_button)
        self.Bind(wx.EVT_BUTTON, self.OnToggleVolume, volume_button)
        self.Bind(wx.EVT_SLIDER, self.OnSetVolume, self.volume_slide)
        self.Bind(wx.EVT_SLIDER, self.OnSetTime, self.timeslider)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        # Create a Proper layout
        main_box = wx.BoxSizer(wx.VERTICAL)
        time_box = wx.BoxSizer(wx.HORIZONTAL)
        buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        
        
        # Add elements for the time box
        time_box.Add(self.timeslider, 1)
        
        # Add main functionailty buttons and the volume slider to button box
        buttons_box.Add(play_button, flag=wx.RIGHT, border=5)
        buttons_box.Add(pause_button)
        buttons_box.Add(stop_button)
        buttons_box.Add((-1, -1), 1)
        buttons_box.Add(volume_button)
        buttons_box.Add(self.volume_slide, flag=wx.TOP | wx.LEFT, border=5)
        
        #Merge the boxes for the controls
        main_box.Add(time_box, flag=wx.EXPAND | wx.BOTTOM, border=10)
        main_box.Add(buttons_box, 1, wx.EXPAND)
        controlbox.SetSizer(main_box)
        
        # Merge the boxes with the video box
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.videobox, 1, flag=wx.EXPAND)
        sizer.Add(controlbox, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=10)
        self.SetSizer(sizer)
        self.SetMinSize((640, 480))


        #Setting Up the Vlc player
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        self.player.set_media(self.Instance.media_new(url))
        
        #attach the video to the GUI
        self.handle = self.videobox.GetHandle()
        self.player.set_hwnd(self.handle)
        
        #start the vido timer
        self.timer.Start()
        
        #set the video audio
        self.volume_slide.SetValue(self.player.audio_get_volume() / 2)
        
        #center and show the window
        self.Center()
        self.Show()

    

  
    def OnClose(self, evt):

        #closes the video to prevent crashing
        self.player.stop()
        self.timeslider.SetValue(0)
        self.timer.Stop()

        self.Destroy() #Closes the Window

    def OnPlay(self, evt):
        
        #Play the video and start the timer
        self.player.play()
        self.timer.Start()

    def OnPause(self, evt):
        
        #pause the video 
        self.player.pause()

    def OnStop(self, evt):

        #Stops the video and the timer
        self.player.stop()
        self.timeslider.SetValue(0)
        self.timer.Stop()

    def OnTimer(self, evt):
        length = self.player.get_length() # get length of the player
        self.timeslider.SetRange(-1, length) #set the length of slider
    
        time = self.player.get_time()  
        self.timeslider.SetValue(time)
        if time > length - 1000 and length > 0: #stops player if there is less than 1 second left
            #stops the player and timer
            self.player.stop()
            self.timeslider.SetValue(0)
            self.timer.Stop()

    def OnToggleVolume(self, evt):

        is_mute = self.player.audio_get_mute() # get if audio is muted

        self.player.audio_set_mute(not is_mute) # reverse the wheter audio is muted

        self.volume_slide.SetValue(self.player.audio_get_volume() / 2) # updates the volume slider

    def OnSetVolume(self, evt):
        self.volume = self.volume_slide.GetValue() * 2 #sets the volume
        self.player.audio_set_volume(self.volume)
    
    def OnSetTime(self, evt):
        time = self.timeslider.GetValue() #sets the time in the video
        self.player.set_time(time)

            


app_alive = False                
main_game = True # sets main game to True
while main_game:
    print("\nSuper Smash Bros Character Gameplay Finder 5000")
    #asks user if they want to Start get Help or Exit
    main_menu = getOptionExit('\nPlease Select an Option',['Start','Help']) 
    
    if main_menu == "Start":
        
        Video_manager = Youtube_Data() # intialize the Youtube data
        mode_loop = Video_manager.getVideos() # Get the list of Videos by asking Use Question and utilizing API
        
        while mode_loop: # runs the main code of the application
            menu_option = getOptionExit('\nWhat would you like to do?', ['View Matches','Change Search Settings','Clear History']) 
            
            if menu_option == 'View Matches':
                if Video_manager.character_vids[0] == []: # Checks if there are no videos
                    print("\n There are no Videos in this categeory or you have watched all of them\n If you want to rewatch a video clear your history")
                    vid_watching = False
                else:
                    vid_watching = True
                    
                while vid_watching: # runs while vid watching True
                    if len(Video_manager.character_vids[0]) <= 10: # runs if less than 10 videos
                        video_option = getOptionNumExit('\nWhich video would you like more info for?\n',Video_manager.character_vids[0])
                    if len(Video_manager.character_vids[0]) > 10:# runs if more than 10 videos
                        video_option = getOptionNumExitMultiPage('\nWhich video would you like more info for?\n',Video_manager.character_vids[0])
                    if video_option == None:# if user chose exit end loops
                        vid_watching = False
                    else: 
                        
                        vid_info = True #loop to ask to watch
                        
                        video_title = Video_manager.character_vids[0][video_option] # GEts the videos title
                        url = 'https://www.youtube.com/watch?v=' +  Video_manager.character_vids[1][video_option] # gets videos url
                        
                        Video_manager.youtube_video_info(Video_manager.character_vids[1][video_option]) # Display info for video
                        
                        while vid_info: # runs while user wants to watch video
                            
                            vid_do = getOptionNumExit('\nWhat would you like to do with this video?\n',['Stream to Computer','Open Link in Youtube'])
                            
                            if vid_do == 0: # if user would like to stream video to computer
                                try:   
                                    
                                    #Get the best version of url to play                         
                                    video = pafy.new(url)
                                    best = video.getbest()
                                    playurl = best.url
                                    
                                    #creates an app if it has not been created before
                                    if not app_alive:
                                        app = wx.App()
                                        
                                    #Creates a Window to play the video    
                                    Window = YoutubePlayer(video_title,playurl)
                    
                                    
                                    #adds video to history
                                    Video_manager.history.append(video_title)
                                    Video_manager.writeFileHistory()
                                    
                                    #Runs the Window until it is closed
                                    print("\nClose the Video Player in order to Continue the Application\n")
                                    app.MainLoop()
                                    app_alive = True
                                    
                                except BaseException: # if video cannot stream
                                    print('\n This computer does not support the vlc functionality to stream the video\n')
                                    
                            elif vid_do == 1: # if user would like to open the video in youtube
                                
                                webbrowser.open_new(url) # opens in default browser
                                
                                #adds video to history
                                Video_manager.history.append(video_title)
                                Video_manager.writeFileHistory()
                            else:
                                vid_info = False

                    
                #Oncer user is done watching videos write them to text 
                Video_manager.writeFileHistory()
                Video_manager.getFileHistory()
                Video_manager.hide_oldvids()

            elif menu_option == 'Change Search Settings':
                Video_manager.getVideos() # get Whataver videos the user wants
                
            elif menu_option == "Clear History":
                print('\n Loading...\n') # accesses Youtube Api for new videos which takes time
                
                #Clears history in text file
                Video_manager.clearFileHistory()
                #updates history data 
                Video_manager.getFileHistory()
                
                #searches for the character videos once more
                Video_manager.youtube_search() 
                Video_manager.character_vidfinder(Video_manager.videos)
                print('\nYour File History has been cleared\n')
                
            else:
                #stops loop
                mode_loop = False
                
                
        
                
    elif main_menu == "Help":
        showHelp() #shows in-game help through a series of print statments
    else:
        main_game = False # set main game ot flase
        print("\nProgram Exited") #tells user they have exited the program
        
if app_alive: # if the was run the run app.Main loop
    app.MainLoop()

