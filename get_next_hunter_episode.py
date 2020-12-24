import browserhistory as bh
import sys

class Show_data:

    def __init__(self,show):

        self.valid_shows = {"hunter"}

        self.cur_show = show

        #map show to official title
        self.show_to_title = {"hunter": 'Hunter x Hunter (2011)'}

        #map for dash number that represents start of episode
        self.show_episode_dash = {"hunter":5,"naruto":4} 
        
        #largest valid episode
        self.max_show_episode = {"hunter":'148'} 


        #set of valid shows to use
        

    def verify_show(self):
        if self.cur_show not in self.valid_shows:
            return False
        return True

    def get_title(self):
        return self.show_to_title[self.cur_show]
    
    def get_episode_dash(self):
        return int(self.show_episode_dash[self.cur_show])
    
    def find_dash_idx(self,entry_url,num_dash):
        idx = -1

        for _ in range(0,num_dash):
            idx = entry_url.find('-',idx+1)

        return idx

    def get_max_episode(self):
        return self.max_show_episode[self.cur_show]
    
    def verify_valid_episode(self,cur_episode):
        return cur_episode <= int(self.max_show_episode[self.cur_show])

    
    
    

def is_correct_entry(entry,show_data,counter):

    entry_title = entry[1]
    
    #if i'm scaling this up to work for all streaming services, I need to return a list of titles to match with
    target_title = show_data.get_title() 

    if len(target_title) > len(entry_title):
        return False

    if entry_title[0:len(target_title)] == target_title:
        return True

    counter += 1 
    return False


def get_episode_num(entry_url,dash_idx):
    #dash_idx initially points to dash right before episode number, so increment once
    dash_idx += 1
    episode_num = ""
    while entry_url[dash_idx] != '-':
        episode_num += entry_url[dash_idx]
        dash_idx += 1


    return int(episode_num)



def get_next_url(entry,show_data):
    entry_url = entry[0]
    
    dash_num = show_data.show_episode_dash[show_data.cur_show]
    dash_idx = show_data.find_dash_idx(entry_url, dash_num)

    cur_episode = get_episode_num(entry_url,dash_idx)
    cur_episode += 1

    if show_data.verify_valid_episode(cur_episode) == False:
        print("Episode does not exist")
        exit(1)

    return create_new_url(cur_episode,entry_url,dash_idx,show_data)

def create_new_url(cur_episode, entry_url, dash_idx,show_data):
    new_url = entry_url[0:dash_idx]
    new_url += '-' + str(cur_episode)

    next_dash_idx = show_data.get_episode_dash() +1

    second_substr_idx = show_data.find_dash_idx(entry_url,next_dash_idx)

    new_url += entry_url[second_substr_idx:]

    return new_url

def main():
    cur_show = sys.argv[1]

    NUM_SEARCH = 1000 #look through last x history entries

    show_data = Show_data(cur_show)

    if show_data.verify_show() == False:
        print("Bad show...")
        exit(1)


    history_dict = bh.get_browserhistory() 
    safari_history_list = history_dict['safari'] #Make usable for other browswers too 
    
    next_url = None

    counter = 0

    for search_idx in range(NUM_SEARCH):
        entry = safari_history_list[search_idx]

        entry_url = entry[1] 
        if entry_url != None and is_correct_entry(entry,show_data,counter):
            next_url = get_next_url(entry,show_data)

            print(next_url)
            exit(0)

        counter += 1

    print(f"Episodes not found in history. Searched {NUM_SEARCH} entries")
    exit(1)

        
main()

