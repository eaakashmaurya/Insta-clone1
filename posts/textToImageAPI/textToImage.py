from PIL import Image, ImageDraw, ImageFont
import numpy as np
import glob
from datetime import datetime

def textToImage(txtArray,profile_id):
    Nimages = len(glob.glob1('./media/textToImageAPI',"back*"))
    DiceRoll = np.random.randint(1,Nimages+1)
    image = Image.open('./media/textToImageAPI/back'+str(DiceRoll)+'.jpg')
    width, height = image.size
    draw = ImageDraw.Draw(image)
    fontSanskrit = ImageFont.truetype('./media/textToImageAPI/ARIALUNI.TTF', size=45)
    (startX, startY) = (width//10, height//10)
    rangeX = width - 2*startX
    for txt in txtArray:
        words = txt.split(' ')
        currentX = startX; currentY=startY;
        message=''
        line=''
        i=0
        nlines=1
        while(i<len(words)):
            lengthCurrentLine = fontSanskrit.getlength(line+words[i])
            if lengthCurrentLine > rangeX:
                nlines+=1
                message += line+'\n'
                line=''
            else:
                line+=' '+words[i]
                i+=1
        message += line
        color = 'rgb(255, 255, 255)' # black color
        heightMsg = fontSanskrit.getsize(message)[1] * (nlines+1)
        # draw the message on the background
        draw.text((startX, startY), message, fill=color, font=fontSanskrit)
        startY = startY + heightMsg
    # save the edited image
    timenow = datetime.now()
    timenow = timenow.strftime("%Y%m%d%H%M%S")
    pathToSave = profile_id+'_'+timenow+'.png'
    image.save('./media/posts/photos/'+pathToSave)
    return pathToSave