from PIL import Image, ImageDraw, ImageFont
import numpy as np
import glob

def textToImage(txtArray):
    Nimages = len(glob.glob1('.',"back*"))
    DiceRoll = np.random.randint(1,Nimages+1)
    image = Image.open('back'+str(DiceRoll)+'.jpg')
    width, height = image.size
    draw = ImageDraw.Draw(image)
    fontSanskrit = ImageFont.truetype('./ARIALUNI.TTF', size=45)
    fontEnglish = ImageFont.truetype('arial.ttf',size=45)
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
    image.save('finalImage.png')


txt = "संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम्"
txt3 = "संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम् संस्कृतम्"
txt2 = "This is some english bullshit, we want to check a long sentence in english how does that wrok. my name is dipanshu I know"
textToImage([txt,txt2,txt3])