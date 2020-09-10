import requests
import bs4
import tkinter as tk
import plyer
import time
import threading


def get_website_data(url) :
    data = requests.get(url)
    return data


def get_website_detail() :
    url = "https://www.mohfw.gov.in/"
    html_data = get_website_data(url)

    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_div = bs.find("div", class_="site-stats-count").find('ul').find_all('li')
    all_detail = ""
    for item in info_div[0 :4] :
        count = item.find('strong').get_text()
        text = item.find('span').get_text()
        all_detail += text + " : " + count + "\n"

    return all_detail


def refresh_button() :
    newdata = get_website_detail()
    print("Processing..")
    myLable['text'] = newdata


def notification() :
    while True :
        plyer.notification.notify(
            title='New COVID-19 Cases',
            message=get_website_detail(),
            timeout=10,
        )
        time.sleep(30)


root = tk.Tk()
root.geometry("900x800")
# root.iconbitmap("Corona Icon.ico")
root.title('Corona Cases Tracker - India')
root.configure(background='white')
f = ("poppins", 25, "bold")

# corona_image = tk.PhotoImage(file='Corona Image.png')
# corona_image_lable = tk.Label(root, image=corona_image)
# corona_image_lable.pack()


myLable = tk.Label(root, text=get_website_detail(), font=f, bg='white')
myLable.pack()

button = tk.Button(root, text="REFRESH", font=f, relief='solid', command=refresh_button)
button.pack()

th1 = threading.Thread(target=notification)
th1.setDaemon(True)
th1.start()

root.mainloop()
