# Proposal

## What is it 

LB2LCNC is a python program that runs locally on the machine that runs LinuxCNC. It accepts commands & g-code via TCP from a Lightburn (LB) instance. It also sends status information back to LB.

## Commands

Commands from LB will be parsed and sent via pylib to LCNC.

Python interface:
https://linuxcnc.org/docs/master/html/de/config/python-interface.html

## G-Code

G-code from LB is saved as a whole in a temporary file. The code is then started/stopped/paused... by commands from LB.

## Problems

* I haven't found a documentation on how LB creates g-code
* when you press start in LB, the wholde gcode is sent out. I don't know how to control this. LB assumes the program has run its course and does not react to stop or pause.
