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
    client.publish("game/ready", 0)
    starttime = time.time()


def finishgame():
    global p1, p2, ingame
    if p1.points > p2.points:
        client.publish("game/finished", 1)
    elif p1.points < p2.points:
        client.publish("game/finished", 2)
    elif p1.points == p2.points:
        client.publish("game/finished", 0)
    p1.clear()
    p2.clear()
    ingame = False


def on_message(client, userdata, message):
    global p1, p2, ingame, starttime
    if message.topic == "player1/ready":
        p1.ready()
        if p2.ifready:
            startgame()
    elif message.topic == "player2/ready":
        p2.ready()
        if p1.ifready:
            startgame()
    elif message.topic == "player1/quit":
        p1.quit()
        if ingame:
            finishgame()
    elif message.topic == "player2/quit":
        p2.quit()
        if ingame:
            finishgame()

    elif message.topic == "Akcelerometr/Down" and ingame:
        p1.addpoint()
        client.publish("player1/points", p1.points)
        if abs(starttime - time.time()) > 20:
            finishgame()
    elif message.topic == "AkcelerometrBur/Down" and ingame:
        p2.addpoint()
        client.publish("player2/points", p2.points)
        if abs(starttime - time.time()) > 20:
            finishgame()


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
    pass

client.loop_stop()  # stop the loop
client.disconnect(broker_address)
