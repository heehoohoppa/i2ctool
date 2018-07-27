# **Structure for the I2C Interface** #

This document outlines the development cycle of the I2C Interface project.
It outlines the .py files included in the whole project, and what each one
actually does.

## **main.py** ##
Acts as the main method. Will orchestrate the command line interface and calling
the required functions. Is gonna have a lot of includes in it.

## **xtlogin.py** ##
Will contain a class for interacting with the blade controller. This class should
be usable from anywhere, and will likely be passed as arguments to basically 
everything there is.

## **csvlib.py** ##
Stores all the information on the individual I2C devices. Handles reading from the
CSV and comparing to the devices actually present on the board.
Needs to have a good level of forward-compatibility or else this application will be basically useless.
This file will probably have the most code in it, just because of the size of
everything involved.

For reading in the I2C devices:

* Have a function run through the /sys/bus/i2c/devices/* folder and populate everything that way.
* Now check the read-in list against the excel sheet and form your present/not present list that way.
    * Should create a framework that functions, then figure out how to make it correct.

## **helperFunctions.py** ##
This file will have all the functions called by main.py. It'll be a time.
Have fun with all of this! I believe in you!



# Functions #
* Global
    * exit
    * set_cname
    * get_ps
    * adv_ps
    * cmd
    * help
* Board
    * get_board
    * read_excel
    * goto_bus
    * buses/bus_list/i2cdetect
    * walk_bus
    * pop_by_type
* Bus
    * walk_bus/walk/pop/populate
    * get_device
    * disp_types
    * send_cmd
* Device
    * watch/monitor
    * get_reg
    * set_reg
    * get_prop
    * set_prop