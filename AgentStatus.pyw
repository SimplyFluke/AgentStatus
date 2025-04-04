import re
import json
import urllib3
import requests
from tkinter import *
from time import sleep
from time import strftime
from threading import Thread

urllib3.disable_warnings()

agentStateDict = {1: "Logged Off", 2: "Ready", 3: "Not Ready"}
callStateDict = {-1: "Logged Off", 1: "Idle", 2: "Alerting", 3: "Talking", 5: "Clerical"}
stop_thread = False

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
        

def getQueue():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36", 
            "Referer": "__Removed__",
            "Accept": "application/json;charset=utf-8"}

    r = requests.get("__Removed__", headers=headers, verify=False)

    return json.loads(json.dumps(r.json()[0]["Data"][1]))


def getAgentInfo():
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36", 
            "Referer": "__Removed__",
            "Accept": "application/json;charset=utf-8"}
    r = requests.get("__Removed__", headers=headers, verify=False)

    agentInfo = json.loads(json.dumps(r.json()[0]["Data"]))
    
    #Format info
    for i in range(len(agentInfo)):
        name = agentInfo[i]["Agent Name"].split(",")
        fullName = f"{name[1].lstrip()} {name[0]}"
        
        agentInfo[i]["Agent Name"] = fullName
        agentInfo[i]["Agent state"] = agentStateDict[agentInfo[i]["Agent state"]]
        agentInfo[i]["Call state"] = callStateDict[agentInfo[i]["Call state"]]
    
    return agentInfo


def on_closing():
    global stop_thread
    stop_thread = True
    thread.join()
    root.destroy()
    quit()


def updateUI():   
    while stop_thread == False: 
        textColor = {"Logged Off": "Red", "Idle": "Green", "Talking": "Yellow", "Ready": "Green", "Not Ready": "Orange", "Outgoing": "Orange", "Clerical": "Pink", "Alerting": "Yellow"}
        agents = getAgentInfo()
        queue = getQueue()
        ypos = 30
        for agent in agents:
            # Create ID to give unique name to labels
            agentID_setup = re.findall("[A-Z]+", agent["Agent Name"])
            agent_ID = ""
            
            for char in agentID_setup:
                agent_ID += char

            callState = agent["Call state"]
            agentState = agent["Agent state"]
            nameLabel = Label(root,name=f"{agent_ID.lower()}1", text=str(agent["Agent Name"]), font="Verdana 9",foreground="snow", background="gray26")
            agentStateLabel = Label(root, name=f"{agent_ID.lower()}2", text=str(agentState), font="Verdana 9",foreground="snow", background="gray26")
            callStateLabel = Label(root,name=f"{agent_ID.lower()}3", text=str(callState), font="Verdana 9",foreground="snow", background="gray26")

            agentStateLabel.configure(fg=textColor[agentState])
            callStateLabel.configure(fg=textColor[callState])
            
            nameLabel.place(x=10, y=ypos)
            agentStateLabel.place(x=200, y=ypos)
            callStateLabel.place(x=300, y=ypos)
            
            ypos += 20

        callsInQueue = Label(root, name="callsInQueue", text=queue["Calls in queue"], font="Verdana 10 bold", foreground="snow", background="gray26")
        longestWaitingTime = Label(root, name="longestWaitingTime", text=queue["Longest waiting time"], font="Verdana 10 bold", foreground="snow", background="gray26")
        callsToday = Label(root, name="callsToday", text=queue["Calls today"], font="Verdana 10 bold", foreground="snow", background="gray26")
        serviceLevel = Label(root, name="serviceLevel", text=f"{queue['Service level']}%", font="Verdana 10 bold", foreground="snow", background="gray26")
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

        root.title(f'AgentStatus :) - {strftime("%H:%M:%S")}')
        sleep (10)


thread = Thread(target=updateUI, daemon=False)
thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
