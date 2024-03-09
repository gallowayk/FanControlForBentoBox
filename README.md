![Full Unit in Place](/Images/IMG_1583.jpg)

After printing out the Bento Box filtration model, I wanted a means to control the fans so they weren't on 24/7 and only enabled when high VOC content was present. Originally, I was only going to use a bimetal temp switch since the ambient internal temperature of the printer would only rise while printing ABS, PC, Nylon, etc. However, I wanted to take a more sophisticated approach while keeping costs low. 

**Electronics**
- RPi Pico (any variant)
- 3.3V trigger opto-isolated relay https://www.amazon.com/dp/B07XGZSYJV 
- MS1100 gas sensor https://www.amazon.com/dp/B0BF4JDW26
- AHT21 temperature and humidity sensor https://www.amazon.com/HiLetgo-Precision-Temperature-Humidity-2-0-5-5V/dp/B09KGW1G41/ref=sr_1_1?crid=2S7GDT005PZ1J&dib=eyJ2IjoiMSJ9.9JbgYaCwdJ3Bu2tPpmYO8JT4jBVGgzy2xskd9ds7lU-Vm1S_DRFpFxZ2ed7sxHwDg30RkraO381sEx3rLJTya3kl8IY_m3K5Wu1LMr0MNqB6qxS1xXAolapEOD3HWWfIFsEzPzPEq1cLhgUfoYQDtXXA8q0qkdt0mzQKxfpbpJt0DQKvs_ot3KuqB4Xbm1lcmvbAz9Rb5F-uHQZx1wrLIXnjcj_Q8dowmKgb1OZ9OVE.k4-kCvhVlD0qiWUWE1QeGVfbAW5VqWgz2DAbHSHnM0Q&dib_tag=se&keywords=aht21+humidity+and+temp+sensor&qid=1709663558&sprefix=aht21+humidity+and+temp+sensor%2Caps%2C174&sr=8-1
- 128x64px SSD1306 OLED screen https://www.amazon.com/gp/product/B0833PF7ML 
- LM2596S buck converter https://www.amazon.com/gp/product/B07QKHR6PY 
    - The buck converter must be adjusted to +5VDC or +3/3.3VDC

![Assembled Electronics box](/Images/IMG_1580.jpg)


**Hardware**
- 2x M2x5 or M2x8 self-tapping screw
  - One for VOC sensor
  - One for RPi Pico
- 8x 4x2mm Magnets
- Various jumper wires
- Helps to use male to female jumper wires
- It also helps to have a Dupont connection/terminal kit and crimper; this will allow you to make your own wires of just the right length


**Tools**
- Soldering iron
- TS100 is my go-to due to its rapid heating and cooling
- "Helping hands" for soldering
- Precision tool set
- Ball-end hex keys can be used as well
- Ferrule crimper + ferrules
- Heatshrink

 ![Wiring Diagram](/Images/Diagram.png)


**Note: Please be sure to safely work on your electronics.**

Do not work on anything while power is connected
Do your best to avoid inhaling the flux/solder fumes
 

**Software**
Please read through the entire program to acclimate yourself with the functionality!
Pin definitions can be easily changed at the top from those I chose to use.
For those who haven't used Raspberry Pis for their own scripts, save “main.py” to your RPi Pico. When power is applied, this program will run automatically. 

For the program to run you need to also install some packages to the pico board as follow
 - picozero
 - ssd1306 (for the led screen)
 - time
 - typing_extensions
 - micropython_ahtx0 (for the external temp sensor)

 Recomended to use the [Thonny IDE](https://thonny.org/) for package management and connection to the pico

 Before uploading the main.py you need to install the micropython firmware to the pico more details [MicroPython Downloads](https://micropython.org/download/) please select your model from the list.

When I have a bit more time, I'll create a full write up with instructions on how to connect everything. Until then, feel free to ask me questions. Please note, however, that I may not be able to respond quickly.
There are still some tweaks I'd like to make, so a revision may come at some point. I want to reduce the clutter in the electronics housing by utilizing integrated solutions or developing my own PCB with an RP2040 chip and on-board power handling.
