import paho.mqtt.client as mqtt  # import the client1
import time
import player

p1 = player.Player(1)
p2 = player.Player(2)
starttime = None
ingame = False


def startgame():
    global ingame, client, starttime
    ingame = True
    client.publish("Master/Ready", 0)
    starttime = time.time()


def finishgame():
    global p1, p2, ingame
    if p1.points > p2.points:
        client.publish("Win/Player1", 1)
    elif p1.points < p2.points:
        client.publish("Win/Player1", 2)

    p1.clear()
    p2.clear()
    ingame = False


def on_message(client, userdata, message):
    global p1, p2, ingame, starttime
    if message.topic == "Ready/Player1":
        p1.ready()
        if p2.ifready:
            startgame()
    elif message.topic == "Ready/Player2":
        p2.ready()
        if p1.ifready:
            startgame()
    elif message.topic == "Player/Quit":
        p1.quit()
        p2.quit()
        if ingame:
            finishgame()

    elif message.topic == "Akcelerometr/Down" and ingame and abs(starttime - time.time()) > 5:
        p1.addpoint()


    elif message.topic == "AkcelerometrBur/Down" and ingame and abs(starttime - time.time()) > 5:
        p2.addpoint()



########################################


broker_address = "192.168.0.180"
client = mqtt.Client("receiver_game")  # create new instance
client.on_message = on_message  # Przerwanie przy dostaniu wiadomosci
client.connect(broker_address)
client.loop_start()  # start the loop
client.subscribe("player1/ready")
client.subscribe("player2/ready")
client.subscribe("player1/quit")
client.subscribe("player2/quit")
client.subscribe("Akcelerometr/Down")
client.subscribe("AkcelerometrBur/Down")

while True:
    if ingame and starttime:
        if abs(starttime - time.time()) > 25:
            finishgame()
    pass

client.loop_stop()  # stop the loop
client.disconnect(broker_address)
