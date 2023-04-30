![alt text](https://github.com/trvrenglish/SpotiPi/blob/main/SpotiPiLogo.png?raw=true)

HARDWARE USED
	Raspberry pi zero w v1.1
	ADS1115
	MAX4466
	Wiring and soldering
Steps for software
	Install raspberry pi os on the raspberry pi
	Install circuitpy and enable i2c via raspi-config
	Clone the repository here
	Run the shell shell script which initializes the db
Wiring
	Pinout commands exist for the raspberry pi, it will be useful for reference
	For the Max4466
	Connect VCC to 3.3V power
Connect the GND to ground
Connect the output to the a0 analog input on the ADS1115.
	For the ADS1115
		Connect VCC to 3.3V power
	Add a 0.1uF bipolar transistor as a buffer between VCC and a different ground pin on the pi. This helps to regulate any fluctuations in the incoming voltage from the pi.See the ADS1115 datasheet for more information.
	Connect the GND to ground
	Connect SDA to pin 3 (GPIO2)
	Connect SCL to pin 5 (GPIO3)
