import time
import cv2
import mss
import numpy
import pytesseract
import re
from discord import SyncWebhook
import sys

URL_TEST_CHANNEL = ''
TAG_PK = '<@&1030657744950276177>  '

def is_a_pk_message(message):
    message_parts = re.findall("\w+", message)
    last_parts = []
    if (len(message_parts) > 4):
        last_parts = message_parts[-5:]
        last_parts = list(map(lambda x : nospecial(x).lower(), last_parts))
        last_parts = list(map(lambda x : "liberty" in x, last_parts))
    return len(message_parts) >= 10 and 'defeated' in message_parts and any(last_parts)      
    
def get_monitor(sct):
    selected = None
    monitor_number = 2
    mon = sct.monitors[monitor_number]
    monitor1 = {'top': 155, 'left': 450, 'width': 960, 'height': 40, 'monitor': 1}
    monitor2 = {'top': mon["top"] + 155, 'left': mon["left"] + 450, 'width': 960, 'height': 40, 'monitor': 2}
    try:
        selected = int(sys.argv[1])
    except:
        selected = 1
    return monitor1 if selected == 1 else monitor2 
    
def nospecial(text):
  text = re.sub("[^a-zA-Z0-9 ]+", "", text)
  return text
      
with mss.mss() as sct:
    monitor = get_monitor(sct)
    print(monitor)
    while True:
        im = numpy.asarray(sct.grab(monitor))
        message = pytesseract.image_to_string(im)
        is_pk_message = is_a_pk_message(message)
        if is_a_pk_message(message): 
            message = nospecial(message)
            print(message)
            webhook = SyncWebhook.from_url(URL_TEST_CHANNEL)
            webhook.send(TAG_PK + message)
            time.sleep(1)
        cv2.imshow('Image', im)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        time.sleep(1)


        
        
