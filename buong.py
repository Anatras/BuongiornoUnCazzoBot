from pyrogram import Client, Filters, Emoji
from pyrogram.errors import UsernameNotOccupied

import json
import schedule, time
import random
import threading
import re

running = True
chatIDs = []
BannatiID = []
messaggiBuongiornoGruppi = []
messaggiBuongiornoPVT = []

#apri file json e inserisci dati nelle liste
with open('AllChats.json') as json_file:  
    chatIDs = json.load(json_file)
with open('BannatiID.json') as json_file:  
    BannatiID = json.load(json_file)
with open('BuongiornoPVT.json',encoding='utf-8') as json_file:  
    messaggiBuongiornoPVT = json.load(json_file)
with open('BuongiornoGroup.json',encoding='utf-8') as json_file:  
    messaggiBuongiornoGruppi = json.load(json_file)



app = Client(
    "BuongiornoUnCazzo",
    bot_token="TOKEN"
)


def BuongiornoUnCazzo():
    for utente in chatIDs:
        if app.get_chat(utente).type != "private":
            messaggio = random.choice(messaggiBuongiornoGruppi)
            if "{}" in messaggio:
                title = app.get_chat(utente).title
                messaggio = messaggio.format(title)
        else:
            messaggio = random.choice(messaggiBuongiornoPVT)
        app.send_message(utente,messaggio)

#funzione per far funzionare le schedule
def scheduleStart():
    while running==True:
        schedule.run_pending()
        time.sleep(1)

t1 = threading.Thread(target=scheduleStart)
t1.start()

schedule.every().minute.at(":00").do(BuongiornoUnCazzo)

#funzione per salvare le liste nei json
def SaveList(fileName,list):
    with open(fileName, 'w', encoding='utf-8') as outfile:
        json.dump(list, outfile, ensure_ascii=False, indent=2)


@app.on_message(Filters.command(["start"]) | Filters.command(["iscrivimi"]))
def start(client,message):
    global chatIDs
    if message.chat.id not in chatIDs:
        if message.chat.type=="private":
            chatIDs.append(message.from_user.id)
            chatName = message.from_user.first_name
        else:
            chatIDs.append(message.chat.id)
            chatName = message.chat.title

        app.send_message(message.chat.id,f"**{chatName}** ti sei registrato, ogni mattina alle __8.00__ riceverai un messaggio per augurarti una bellissima **giornata del cazzo** {Emoji.SKULL_AND_CROSSBONES}\n\nPer disiscriverti usa il comando `/disiscrivimi`")
        SaveList("AllChats.json",chatIDs)
    else:
        app.send_message(message.chat.id,"Sei già presente nei nostri database\n\nPer disiscriverti usa il comando `/disiscrivimi`")

SaveList("BuongiornoPVT.json",messaggiBuongiornoPVT)
SaveList("messaggiGroup.json",messaggiBuongiornoGruppi)

@app.on_message(Filters.new_chat_members)
def welcome(client,message):
    global chatIDs
    for utente in message.new_chat_members:
        if utente.id==696071937:
            if message.chat.id not in chatIDs:
                chatIDs.append(message.chat.id)
                chatName=app.get_chat(message.chat.id).title
                app.send_message(message.chat.id,f"Il gruppo {chatName} è stato registrato correttamente, ogni mattina alle __8.00__ riceverete un messaggio per augurarvi una bellissima **giornata del cazzo** {Emoji.SKULL_AND_CROSSBONES}\n\nPer disiscriverti usa il comando `/disiscrivimi`")
                SaveList("AllChats.json",chatIDs)
            else:
                app.send_message(message.chat.id,"Il gruppo è già presente nei nostri database\n\nPer disiscriverti usa il comando `/iscrivimi`")

@app.on_message(Filters.command(["disiscrivimi"]))
def disiscrivimi(client,message):
    global chatIDs
    if message.chat.id in chatIDs:
        if message.chat.type=="private":
            chatIDs.remove(message.from_user.id)
            app.send_message(message.chat.id,"Disiscritto con successo.\n\nPer iscriverti nuovamente usa il comando `/iscrivimi`") 
        else:
            if app.get_chat_member(message.chat.id,message.from_user.username).status in ("creator","administrator"):
                indexID = chatIDs.index(message.chat.id)
                del chatIDs[indexID]
                app.send_message(message.chat.id,"Disiscritto con successo.\n\nPer iscriverti nuovamente usa il comando `/iscrivimi`")          

            else:
                app.send_message(message.chat.id,"Solo gli **admin** possono discrivere il canale")
        SaveList("AllChats.json",chatIDs) 
    else:
        app.send_message(message.chat.id,"Sei già disiscritto!\n\nPer iscriverti nuovamente usa il comando `/iscrivimi`")

@app.on_message(Filters.command(["invia"]) & Filters.user("Anatras02"))
def inviaMSG(client,message):
    messaggio = message.command[1:]
    messaggio = " ".join(messaggio)
    for utenteID in chatIDs:
        app.send_message(utenteID,messaggio)
    app.send_message(message.chat.id,"Messaggi inviati con successo!")

@app.on_message(Filters.command(["consiglia"]))
def inviaMSG(client,message):
    if message.from_user.id in BannatiID:
        app.send_message(message.chat.id,"Hai abusao del sistema dei suggerimenti e sei stato bannato.\n\nSe pensi sia stato"+
            " un errore contatta @Anatras02 in chat privata.")
    else:
        messaggio = " ".join(message.command[1:])
        app.send_message("Anatras02",f"#suggerrimento\n\n`{messaggio}`\n\nby @{message.from_user.username}")
        message.reply("Suggerrimento inviato con successo, se il suggerimento dovesse essere accettato verrai "+
            "contattato da @Anatras02")

@app.on_message(Filters.command(["ban"]) & Filters.user("Anatras02"))
def ban(client,message):
    try:
        userID = app.get_chat(message.command[1]).id
        if userID in BannatiID:
            messagge.reply("Utente già bannato!\nSbannalo con /unban nome utente")
        else:
            BannatiID.append(userID)
            message.reply("Utente bannato con successo!")
            SaveList("BannatiID.json",BannatiID)
    except UsernameNotOccupied:
        message.reply("L'utente non esiste")

@app.on_message(Filters.command(["unban"])  & Filters.user("Anatras02"))
def unban(client,message):
    userID = app.get_chat(message.command[1]).id
    if userID not in BannatiID:
        messagge.reply("Utente non bannato! Per bannarlo usa il comando /ban")
    else:
        indexID = BannatiID.index(userID)
        del BannatiID[indexID]
        message.reply("Utente sbannato!")
        SaveList("BannatiID.json",BannatiID)

@app.on_message(Filters.command(["lista"]))
def lista(client,message):
    buongiornoGrupSTR = "**Gruppi: **\n"
    buongiornoPVTSTR = "**Privato: **\n"
    for buongiorno in messaggiBuongiornoGruppi:
        if "{}" in buongiorno:
            buongiorno = buongiorno.format("NOME")
        buongiornoGrupSTR = buongiornoGrupSTR + "> " + buongiorno + "\n"

    for buongiorno in messaggiBuongiornoPVT:
        buongiornoPVTSTR = buongiornoPVTSTR + "> " + buongiorno + "\n"

    app.send_message(message.chat.id,buongiornoGrupSTR+"\n"+buongiornoPVTSTR)

@app.on_message(Filters.command(["agg"]) & Filters.user("Anatras02"))
def lista(client,message):
    rx = r'/agg\s+(pvt|gruppo)\s+(.+)'
    mo = re.match(rx, message.text)
    if mo:
        if mo.group(1).lower()=="gruppo":
            if mo.group(2) not in messaggiBuongiornoGruppi:
                messaggiBuongiornoGruppi.append(mo.group(2))
                SaveList("BuongiornoGroup.json",messaggiBuongiornoGruppi)
                message.reply("Messaggio aggiunto!")
            else:
                app.send_message(message.chat.id,"Messaggio già esistente")

        elif mo.group(1).lower()=="pvt":
            if mo.group(2) not in messaggiBuongiornoPVT:
                messaggiBuongiornoPVT.append(mo.group(2))
                SaveList("BuongiornoPVT.json",messaggiBuongiornoPVT)
                message.reply("Messaggio aggiunto!")
            else:
                app.send_message(message.chat.id,"Messaggio già esistente")
    else:
        app.send_message(message.chat.id,"Formato sbagliato!\n\n/agg pvt/gruppo messaggio")

@app.on_message(Filters.command(["rimuovi"]) & Filters.user("Anatras02"))
def lista(client,message):
    rx = r'/rimuovi\s+(pvt|gruppo)\s+(.+)'
    mo = re.match(rx, message.text)
    if mo:
        if mo.group(1).lower()=="gruppo":
            if mo.group(2) in messaggiBuongiornoGruppi:
                indexID = messaggiBuongiornoGruppi.index(mo.group(2))
                del messaggiBuongiornoGruppi[indexID]
                SaveList("BuongiornoGroup.json",messaggiBuongiornoGruppi)
                message.reply("Messaggio rimosso!")
            else:
                app.send_message(message.chat.id,"Messaggio non presente, non posso rimuoverlo")

        elif mo.group(1).lower()=="pvt":
            if mo.group(2) in messaggiBuongiornoPVT:
                indexID = messaggiBuongiornoPVT.index(mo.group(2))
                del messaggiBuongiornoPVT[indexID]
                SaveList("BuongiornoPVT.json",messaggiBuongiornoPVT)
                message.reply("Messaggio rimosso!")
            else:
                app.send_message(message.chat.id,"Messaggio non presente, non posso rimuoverlo")
    else:
        app.send_message(message.chat.id,"Formato sbagliato!\n\n/rimuovi pvt/gruppo messaggio")


app.run()

running = False
t1.join()