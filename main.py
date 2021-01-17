import paho.mqtt.client as mqtt  # import the client1
import time
import player

p1 = player.Player(1)
p2 = player.Player(2)


def on_message(client, userdata, message):
    global p1, p2
    if message.topic == "player1/ready":
        pass

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

client.loop_stop()  # stop the loop
client.disconnect(broker_address)
