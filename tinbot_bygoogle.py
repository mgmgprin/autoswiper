from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from login_details_by_google import email, password
import datetime

# 【概要】
# google経由でのログイン
# スワイプの自動化、一回の実行に対するスワイプする回数の指定が可能
# 距離、除外したいワードの有無、プロフに記載があるかなどの条件に応じてNope可能
# ランダムに出現する広告ポップアップの無効化に対応
# マッチ成立後の自動メッセージ送信が可能
# 曜日によってメッセージ内容を変更可能
# 1回目のみ日曜日までに返信が来ていなかったユーザーに対してリマインド送信が可能

class TinderBot():
    exclude_texts = [
                    '除外したいワードを入力してください',
                    '除外条件は複数指定可能です'
                     ]
    
    def __init__(self):
        self.driver = webdriver.Chrome()
    def open_tinder(self):
        self.driver.get('https://tinder.com')
        # self.driver.maximize_window()
        sleep(3)         
        try:
            cookies_accept_button = self.driver.find_element('xpath', '/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/button')
            cookies_accept_button.click()   
        except:
            print('no cookies button')
            
        sleep(5)
        
        login = self.driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]')
        login.click()
        sleep(3)
        self.google_login()

        sleep(10)
        try:
            allow_location_button = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div/div/div[3]/button[1]')
            allow_location_button.click()
        except:
            print('no location popup')
        sleep(3)    
        try:
            notifications_button = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div/div/div[3]/button[2]')
            notifications_button.click()
        except:
            print('no notification popup')
            
    
    def google_login(self):
        # find and click Google login button
        login_with_Google = self.driver.find_element('xpath', '/html/body/div[2]/main/div/div/div[1]/div/div/div[3]/span/div[1]/div/div/div/iframe')
        login_with_Google.click()

        # save references to main and Google windows
        sleep(2)
        base_window = self.driver.window_handles[0]
        google_popup_window = self.driver.window_handles[1]
        # switch to Google window
        self.driver.switch_to.window(google_popup_window)
        # login to Google
        email_field = self.driver.find_element('xpath', '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input')
        login_button = self.driver.find_element('xpath', '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button')
        # enter email, password and login
        email_field.send_keys(email)
        sleep(3)
        login_button.click()
        # 文字認証が必要な場合があるので、その際は手動認証を行ってください
        print('手動でログインしてください...')
        
        sleep(20)
        pw_field = self.driver.find_element('xpath', '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input')
        pw_field.send_keys(password)
        sleep(3)
        self.driver.switch_to.window(base_window)
        
        
    def right_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_RIGHT)
        
    def left_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_LEFT)
        
    def show_profile(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.UP)
        
    def auto_swipe(self):
        number_of_swipes = 50
        target = ' '
        sleep(5)
        for i in range(number_of_swipes):
            print(str(i) + '人目')
            sleep(2)
            try:
                distance = self.driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div/div[2]/div[3]/div/div[2]/div/div/div/div[2]')
                print(distance.text)
                idx = distance.text.find(target)
                try:
                    int_distance = int(distance.text[:idx])
                except ValueError: 
                    try:
                        distance = self.driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/div[2]')
                        print(distance.text)
                        idx = distance.text.find(target)
                        int_distance = int(distance.text[:idx])
                    except:
                        self.left_swipe()
                        self.close_popup
            except: 
                print('距離が非表示のユーザー')
                self.left_swipe()
                self.close_popup
            
                
            if int_distance > 100:
                print('far away')
                self.left_swipe()
                self.close_popup
            else:
                self.show_profile()
                sleep(2) 
                j = 0
                try:
                    contents = self.driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div')
                    for exclude_text in self.exclude_texts:
                        if exclude_text in contents.text:
                            print('reason：'+ exclude_text)
                            self.left_swipe()
                            self.close_popup()
                            j = 1                       
                            break
                except:
                    print('no discription')
                    self.left_swipe()
                    self.close_popup()
                    j = 1
                        
            if j == 0:        
                self.right_swipe()     
                self.close_popup()
                

    def close_popup(self):
        try:
            sleep(1)
            box = self.driver.find_element('xpath', '/html/body/div[2]/main/div/button[2] | /html/body/div[2]/main/div/button[2] | /html/body/div[2]/main/div/div[2]/button[2] | //*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
            box.click()
        except:
            pass

    def get_matches(self):
        match_profiles = self.driver.find_elements(by='class name', value='matchListItem')
        message_links = []
        for profile in match_profiles:
            if profile.get_attribute('href') == 'https://tinder.com/app/my-likes' or profile.get_attribute('href') == 'https://tinder.com/app/likes-you':
                continue
            message_links.append(profile.get_attribute('href'))
        return message_links

    def send_messages_to_matches(self):
        links = self.get_matches()
        for link in links:
            print(link)
            self.send_message(link)

    def send_message(self, link):
        self.driver.get(link)
        sleep(10)
        text_area = self.driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/textarea')
        sleep(3)
        today = datetime.date.today()
        weekday = today.weekday()
        print(weekday)
        if weekday != 6:
            text_area.send_keys('週末以外の初回メッセージ１')
            sleep(1)
            text_area.send_keys(Keys.ENTER)
            sleep(1)
            text_area.send_keys('週末以外の初回メッセージ２')
            sleep(1)
            text_area.send_keys(Keys.ENTER)
        else:
            text_area.send_keys('週末の初回メッセージ１')
            sleep(1)
            text_area.send_keys(Keys.ENTER)
            sleep(1)
            text_area.send_keys('週末の初回メッセージ２')
            sleep(1)
            text_area.send_keys(Keys.ENTER)
  
        
    def roop_plofiles(self):
        links = self.get_links()
        for link in links:
            self.send_remind_messages(link)
            
    def get_links(self):
        match_profiles = self.driver.find_elements(by='class name', value='messageListItem')
        message_links = []
        for profile in match_profiles:
            message_links.append(profile.get_attribute('href'))
        return message_links
    
    def send_remind_messages(self, link):
        self.driver.get(link)
        sleep(10)
        today = datetime.date.today()
        weekday = today.weekday()
        msgObjects = self.driver.find_elements(by='class name', value='msg BreakWord')
        index = len(msgObjects)
        print(index)
        if index <= 2 & weekday == 6:
            text_area = self.driver.find_element('xpath', '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/textarea')
            sleep(3)
            text_area.send_keys('週末に送りたいリマインドメッセージ')  
            sleep(2)
            text_area.send_keys(Keys.ENTER) 
                     

            

bot = TinderBot()
bot.open_tinder()
sleep(10)
bot.auto_swipe()
# bot.send_messages_to_matches()
# bot.send_remind_messages()
