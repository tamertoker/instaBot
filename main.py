import time
from selenium import webdriver
import pickle
import os
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
os.system("clear")


PATH = "C:\Program Files (x86)\chromedriver.exe"



class instaBot:
    def __init__(self, username, password, follower_list, follower_count, follow_list, follow_count):
        self.follower_count = 0
        self.follow_count = 0
        self.username = username
        self.password = password
        self.follower_list = []
        self.follow_list = []
        self.driver = webdriver.Chrome(PATH)

    def giris(self):
        self.driver.get("https://instagram.com")
        un_giris = WebDriverWait(self.driver, 15).until(              # USERNAME GİRİŞ KISMI
            EC.presence_of_element_located((By.NAME, "username")))

        un_giris.send_keys(self.username)
        pw_giris = self.driver.find_element(By.NAME, "password")        # PW GİRİŞ
        pw_giris.send_keys(self.password)
        self.driver.find_element(By.XPATH, "//*[@id='loginForm']/div/div[3]/button").click()
        time.sleep(4)
        save_notif = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/div/div/div/section/div")))
        if save_notif.is_displayed():
            self.driver.find_element(By.XPATH, "/html/body/div[1]/section/main/div/div/div/section/div/button").click()

        hayir = WebDriverWait(self.driver, 15).until(  # NOTIFICATION - NO
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]")))
        hayir.click()
                        # ANA SAYFAYA GİRİŞ YAPTI

    def file_check(self, whatisfor):

        if os.path.isfile(f"{self.username}'s {whatisfor}s.dat"):
            pass
        else:
            print(f"Creating a new {whatisfor} list for {self.username}...") #EĞER DOSYA YOKSA YENİSİNİ OLUŞTURUYOR
            open(f"{self.username}'s {whatisfor}s.dat", "wb")

    def goToProfile(self):
        self.driver.get(f"https://instagram.com/{self.username}")


    def scrapeList(self,whatisfor):

        cikan_liste = self.driver.find_element(By.CLASS_NAME, "_aano")
        scrapings = cikan_liste.find_elements(By.TAG_NAME, "li")  # ÇIKAN LİSTEDEKİ TAKİPÇİ LİSTESİNİ AL
        time.sleep(random.randrange(5, 7))
        whatisforList = [] # içine bi değer atamadan önce boş şekilde tanımlamamız gerekiyor
        whatisforCount = 0
        if whatisfor == "follower":
            whatisforList = self.follower_list
            whatisforCount = self.follower_count
        elif whatisfor == "follow":
            whatisforList = self.follow_list
            whatisforCount = self.follow_count
        else:
            print("Incorrect whatisfor input")

        try: # SİLİNEBİLİR
            while len(whatisforList) < whatisforCount: #listeye eklenen kullanıcı sayısı toplam takipçi sayısını geçmediği sürece
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", cikan_liste)
                    time.sleep(random.randrange(3, 4))
                    users = cikan_liste.find_elements(By.TAG_NAME, "li")
                    for user in users:
                        username = (
                            user.find_element(By.TAG_NAME, "a").get_attribute("href").replace(
                                "https://www.instagram.com/",
                                "")[:-1]) # User ismini yalın şekilde alıyor
                        if username in whatisforList: #INSTA AYNI TAKIPÇIYI KARŞINA BİRDEN ÇOK DEFA ÇIKARDIĞI İÇİN
                            pass
                        else:
                            whatisforList.append(username)
                        try: #DOSYA BOŞ OLURSA EOF ERROR VERİYOR, BU YÜZDEN TRY
                            set(pickle.load(open(f"{self.username}'s {whatisfor}s.dat", "wb+"))).update(set(whatisforList))
                        except EOFError:
                            pickle.dump(whatisforList, open(f"{self.username}'s {whatisfor}s.dat", "wb"))

                    print(f'Got: {len(whatisforList)} usernames of {whatisforCount}. Saved to file.')
            time.sleep(random.randrange(3, 5))


        except OSError:
            raise


    def update_followers(self) :  # UPDATE FOLLOWS KISMINI BUNA KOPYALA

        self.file_check("follower")

        self.goToProfile()
        takipciler = WebDriverWait(self.driver, 15).until(              # PROFİLDEKİ TAKİPÇİLER KISMINI HEDEFLİYORUZ
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div"))
        )
        self.follower_count = int(takipciler.find_element(By.TAG_NAME, "span").get_attribute("title").replace(",", "")) # KAÇ TAKİPÇİ OLDUĞUNUN BİLGİSİNİ ALIYOR
        print(f"Takipçi sayınız: {self.follower_count}")
        takipciler.click()
        time.sleep(random.randrange(8, 10))

        self.scrapeList("follower")

    def update_follows(self):
        self.file_check("follow")
        self.driver.get(f"https://instagram.com/{self.username}")
        takip = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH,
                                                                                 "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[3]/a/div")))
        self.follow_count =int(takip.find_element(By.TAG_NAME, "span").get_attribute("title").replace(",", ""))  # KAÇ TAKİP OLDUĞUNUN BİLGİSİNİ ALIYOR
        print("Takip sayınız:", self.follow_count)
        takip.click()
        time.sleep(random.randrange(8, 10))

        self.scrapeList("follow")

    def follow(self): #KONTROL ET
            whose = str(input("Type the username of the account whose followers you want to follow."))
            self.driver.get(f"https://instagram.com/{whose}/")
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div"))).click()
            time.sleep(3)
            followers = self.driver.find_element(By.CLASS_NAME, "_aano").find_elements(By.TAG_NAME, "li")
            i = 0
            limit = 3
            while i < limit:
                for follower in followers:
                    self.driver.execute_script("arguments[0].scrollIntoView();", follower)
                    takip_edilecek_isim = follower.find_element(By.TAG_NAME, "a").get_attribute("href")
                    if takip_edilecek_isim in pickle.load(open(f"{self.username}'s followers.dat", "rb")):
                        print(takip_edilecek_isim.text, "Zaten takipçi listenizde olduğu için takip edilmedi")
                        continue
                    else:
                        follower.find_element(By.TAG_NAME, "button").click()
                        i += 1
                        time.sleep(random.randrange(5, 8))
            cevap = ""
            if i == limit:
                cevap = str(input("Your daily follow limit is over, do you still want to continue? (risk of getting "
                                  "banned.) (Y or N)"))

            if cevap == "Y":
                limit_increase = int(input("How much would you like to increase your follow limit? (Default = 100)"))
                limit += limit_increase
            else:
                quit()

    def unfollow(self): # CHECK YUKLE BUNA
        self.driver.get("https://instagram.com/%s/" % self.username)
        takip = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[3]/a/div"))
        )
        self.follow_count =int(takip.find_element(By.TAG_NAME, "span").text.replace(",", ""))
        print(self.follow_count)
        takip.click()
        time.sleep(3)

        cikan_liste = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "_aano")))
        follows = cikan_liste.find_elements(By.TAG_NAME, "li")
        def onlyunf():
            onlyunfist = input("Sadece sizi takip etmeyenleri  takipten çıkmak ister misiniz?(Evet için Y, Hayır için N)")
            if onlyunfist == "Y":
                print("Sadece sizi takip etmeyenler takipten çıkılacak.")
            elif onlyunfist == "N":
                print("Takipten çıkma işlemi sırasında kişinin sizi takip etmesi dikkate alınmayacak.")
            else:
                print("Yanlış giriş")
                return(onlyunf())

        limit = int(input("Kaç kişiyi takipten çıkmak istiyorsunuz? (Recommended: 60-300)"))
        if limit > self.follow_count:
            print(f"Girmiş olduğunuz sayı takip sayınızdan büyük. Sadece {self.follow_count} kişi takipten çıkılacak.")
            limit = self.follow_count
        i = 0

        while i < limit:
            for follow in follows:
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", cikan_liste)
                takip_un = (follow.find_element(By.TAG_NAME, "a").get_attribute("href").replace("https://www.instagram.com/", "")[:-1])
                def takiptencikar():
                    time.sleep(random.randrange(8, 13))
                    follow.find_element(By.TAG_NAME, "button").click()
                    try:
                        self.driver.find_element(By.XPATH,
                                                 "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div")
                        self.driver.find_element(By.XPATH,
                                                 "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[1]").click()
                    except:
                        pass
                if follow.find_element(By.TAG_NAME, "button").value_of_css_property('background-color') == "rgba(0, 149, 246, 1)":
                    pass
                if onlyunf == "N":
                    if takip_un in self.follower_list:
                        pass
                    else:
                        print(f"{takip_un} takipçi listenizde olmadığı için takipten çıkarıldı.")
                        takiptencikar()
                        i += 1
                        time.sleep(random.randrange(5, 11))
                else:
                    takiptencikar()
                    i +=1


        if i == limit :
            print(f"İşlem tamamlanıd. {limit}  takipçi çıkarıldı.")

def main():
    my_bot = instaBot


if __name__ == "__main__":
    main()

