![Full Unit in Place](/Images/IMG_1583.jpg)

After printing out the Bento Box filtration model, I wanted a means to control the fans so they weren't on 24/7 and only enabled when high VOC content was present. Originally, I was only going to use a bimetal temp switch since the ambient internal temperature of the printer would only rise while printing ABS, PC, Nylon, etc. However, I wanted to take a more sophisticated approach while keeping costs low. 

**Electronics**
- RPi Pico (any variant)
- 3.3V trigger opto-isolated relay https://www.amazon.com/dp/B07XGZSYJV 
- MS1100 gas sensor https://www.amazon.com/dp/B0BF4JDW26 
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
 


**Note: Please be sure to safely work on your electronics.**

Do not work on anything while power is connected
Do your best to avoid inhaling the flux/solder fumes
 

**Software**
Please read through the entire program to acclimate yourself with the functionality!
Pin definitions can be easily changed at the top from those I chose to use.
For those who haven't used Raspberry Pis for their own scripts, rename “VOC_CKT.py” to “main.py” and save to your RPi Pico.
 

When I have a bit more time, I'll create a full write up with instructions on how to connect everything. Until then, feel free to ask me questions. Please note, however, that I may not be able to respond quickly.
There are still some tweaks I'd like to make, so a revision may come at some point. I want to reduce the clutter in the electronics housing by utilizing integrated solutions or developing my own PCB with an RP2040 chip and on-board power handling.
