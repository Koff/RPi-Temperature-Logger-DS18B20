# RPi-Temperature-Logger-DS18B20

If you want to use your RPi to log temperatures, you will need a couple of things:

* A temp. sensor, I recommend the DS18B20, super easy to install. Stay away from the DHT11 as it has a unique communication protocol
 that requires real-time/interrupts on the GPIO's something that the RPi doesn't have.
 
* A script to log those temperatures. You can use the one in this repo.

## Hardware

Once you get the DS18B20, installation is straight forward. You will need a breadboard, a 4.7K pull-up resistor (+- 20% would also do it) and a couple of wires.
This is a picture of my installation, if you are having troubles on this, I recommend following a wiring diagram like [this](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware) one.

![My circuit](http://s18.postimg.org/wh9phv56x/IMG_20141202_233850_2.jpg)

## Software

After properly connecting the sensor to the RPi, run the following:

```
sudo modprobe w1-gpio
sudo modprobe w1-therm
cd /sys/bus/w1/devices
ls
```

there should be two elements after that `ls`, one named `28*`, that's our sensor. Reading the info from is as simple as accesing a file:
 
```
cd 28 (Press tab to fill the name)
more w1_slave
```

You should then get something like:

```
a2 01 4b 45 7f ff Oe 10 d8 : crc=8 YES
a2 01 ab a6 df ff Oe 10 d8 t=21025
```

The `crc=8 YES` indicates that the temperature was correctly retrieved and the `t=21025` indicates the temperature (multiplied by 1000).

You will also need a MySQL DB, install it and create a database called `temps` then create a table with the following command: 

```
CREATE TABLE `temp_display_temps` (
  `time_stamp` datetime NOT NULL,
  `temperature` decimal(23,8) NOT NULL,
  `comments` varchar(160) NOT NULL,
  `extra` varchar(1) NOT NULL,
  PRIMARY KEY (`time_stamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

I included a couple of extra fields, `comments` and `extra`, this latter one to add a character to label the sensor, in case multiple sensors injecting temps into this table.

At this point the .py script should run, don't forget to edit the information to connect to MySQL.
