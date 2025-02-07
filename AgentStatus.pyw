from tkinter import *
from time import sleep
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

stop_thread = False
chrome_options = Options()
chrome_options.add_argument("--headless=new") # No window
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # shut your up
service = Service(ChromeDriverManager().install())

def insecureClick():
    try:
        avansertButton = driver.find_element(By.XPATH, r"/html/body/div/div[2]/button[3]")
        avansertButton.click()

        proceedButton = driver.find_element(By.XPATH, r"/html/body/div/div[3]/p[2]/a")
        proceedButton.click()
    except:
        pass
    

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("#removed#")
insecureClick()

root = Tk()
root.title("AgentStatus :)")
root.configure(bg="gray26", height=300, width=400)
root.iconbitmap("phone.ico") # https://www.iconarchive.com/show/long-shadow-ios7-icons-by-pelfusion/Phone-icon.html

nameTitle = Label(root, text="Agent Name", font="Verdana 10 bold underline",foreground="snow", background="gray26")
agentStateTitle = Label(root, text="Agent State", font="Verdana 10 bold underline",foreground="snow", background="gray26")
callStateTitle = Label(root, text="Call State", font="Verdana 10 bold underline",foreground="snow", background="gray26")
queueLabel = Label(root, text="Calls in queue:", font="Verdana 10 bold",foreground="snow", background="gray26")
longestWaitLabel = Label(root, text="Longest waiting time:", font="Verdana 10 bold",foreground="snow", background="gray26")
callsTodayLabel = Label(root, text="Calls today:", font="Verdana 10 bold",foreground="snow", background="gray26")
serviceLevelLabel = Label(root, text="Service level:", font="Verdana 10 bold",foreground="snow", background="gray26")
freeAgentsLabel = Label(root, text="Free agents:", font="Verdana 10 bold",foreground="snow", background="gray26")
busyAgentsLabel = Label(root, text="Busy agents:", font="Verdana 10 bold",foreground="snow", background="gray26")

queueLabel.place(x=10, y=220)
longestWaitLabel.place(x=175, y=220)
callsTodayLabel.place(x=10, y=245)
serviceLevelLabel.place(x=175, y=245)
freeAgentsLabel.place(x=10, y=270)
busyAgentsLabel.place(x=175, y=270)
nameTitle.place(x=10, y=10)
agentStateTitle.place(x=190, y=10)
callStateTitle.place(x=300, y=10)


def updateStatus():
    driver.get("#removed#")
    sleep(0.5)
    insecureClick()
    agents = {}
    for i in range(100): # magine 100 ansatte på ITB
        try:
            agentName = driver.find_element(By.XPATH, f"/html/body/div/div/div/div/div/div/table/tbody/tr[{i+1}]/td[1]/span").get_attribute("innerText").split(",")
            agentState = driver.find_element(By.XPATH, f"/html/body/div/div/div/div/div/div/table/tbody/tr[{i+1}]/td[2]/span").get_attribute("innerText")
            callState = driver.find_element(By.XPATH, f"/html/body/div/div/div/div/div/div/table/tbody/tr[{i+1}]/td[3]/span").get_attribute("innerText")
            
            fullName = f"{agentName[1]} {agentName[0]}"
            agents[i] = {"Name": fullName, "Agentstate": agentState, "Callstate": callState}
        except:
            return agents
        

def updateQueue():
    driver.get("#removed#")
    sleep(0.5)
    insecureClick()
    callsInQueue = driver.find_element(By.XPATH, r"/html/body/div/div/div/div/div/div/table/tbody/tr[2]/td[2]").get_attribute("innerText")
    longestWaitingTime = driver.find_element(By.XPATH, r"/html/body/div/div/div/div/div/div/table/tbody/tr[2]/td[3]").get_attribute("innerText")
    callsToday = driver.find_element(By.XPATH, r"/html/body/div/div/div/div/div/div/table/tbody/tr[2]/td[4]").get_attribute("innerText")
    serviceLevel = driver.find_element(By.XPATH, r"/html/body/div/div/div/div/div/div/table/tbody/tr[2]/td[5]").get_attribute("innerText")
    freeAgents = driver.find_element(By.XPATH, r"/html/body/div/div/div/div/div/div/table/tbody/tr[2]/td[6]").get_attribute("innerText")
    busyAgents = driver.find_element(By.XPATH, r"/html/body/div/div/div/div/div/div/table/tbody/tr[2]/td[7]").get_attribute("innerText")
    
    info = {"Calls in queue": callsInQueue, "Longest waiting time": longestWaitingTime, "Calls today": callsToday,
            "Service level": serviceLevel, "Free agents": freeAgents, "Busy agents": busyAgents}
    
    return info


def on_closing():
    global stop_thread
    stop_thread = True
    thread.join()
    root.destroy()
    driver.close()
    quit()


def updateUI():
    while stop_thread == False: 
        textColor = {"Logged Off": "Red", "Idle": "Green", "Talking": "Yellow", "Ready": "Green", "Not Ready": "Orange", "Outgoing": "Orange", "Clerical": "Pink", "Alerting": "Yellow"}
        replaceBadState = {"Invalid (Idle)":"Idle", "Invalid (Ready)": "Ready", "Invalid (Talking)": "Talking", "Invalid (Logged Off)": "Logged Off"}
        agents = updateStatus()
        queue = updateQueue()
        ypos = 30
        for agent in agents:
            callState = agents[agent]["Callstate"]
            agentState = agents[agent]["Agentstate"]
            
            if agentState in replaceBadState.keys():
                agentState = replaceBadState[agentState]
            
            if callState in replaceBadState.keys():
                callState = replaceBadState[callState]

            nameLabel = Label(root,name=f"{agent}1", text=agents[agent]["Name"], font="Verdana 9",foreground="snow", background="gray26")
            agentStateLabel = Label(root, name=f"{agent}2", text=agentState, font="Verdana 9",foreground="snow", background="gray26")
            callStateLabel = Label(root,name=f"{agent}3", text=callState, font="Verdana 9",foreground="snow", background="gray26")

            agentStateLabel.configure(fg=textColor[agentState])
            callStateLabel.configure(fg=textColor[callState])
            
            nameLabel.place(x=10, y=ypos)
            agentStateLabel.place(x=200, y=ypos)
            callStateLabel.place(x=300, y=ypos)
            
            ypos += 20

        callsInQueue = Label(root, name="callsInQueue", text=queue["Calls in queue"], font="Verdana 10 bold", foreground="snow", background="gray26")
        longestWaitingTime = Label(root, name="longestWaitingTime", text=queue["Longest waiting time"], font="Verdana 10 bold", foreground="snow", background="gray26")
        callsToday = Label(root, name="callsToday", text=queue["Calls today"], font="Verdana 10 bold", foreground="snow", background="gray26")
        serviceLevel = Label(root, name="serviceLevel", text=queue["Service level"], font="Verdana 10 bold", foreground="snow", background="gray26")
        freeAgents = Label(root, name="freeAgents", text=queue["Free agents"], font="Verdana 10 bold", foreground="snow", background="gray26")
        busyAgents = Label(root, name="busyAgents", text=queue["Busy agents"], font="Verdana 10 bold", foreground="snow", background="gray26")

        callsInQueue.place(x=120, y=220)
        longestWaitingTime.place(x=340, y=220)
        callsToday.place(x=100, y=245)
        serviceLevel.place(x=280, y=245)
        freeAgents.place(x=105, y=270)
        busyAgents.place(x=275, y=270)

        nameTitle.place(x=10, y=10)
        agentStateTitle.place(x=190, y=10)
        callStateTitle.place(x=300, y=10)
        sleep (10)

thread = Thread(target=updateUI)
thread.start()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
