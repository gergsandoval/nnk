import time
import cv2
import mss
import numpy
import pytesseract
import re
from discord import SyncWebhook
import sys

URL_TEST_CHANNEL = ''
TAG_PK = '<@&1035271414695079946>  '

def is_a_pk_message(message):
    message_parts = re.findall("\w+", message)
    message_parts = list(map(lambda x : nospecial(x).lower(), message_parts))
    appeared_in_parts = list(map(lambda x : 'appeared' in x, message_parts))
    gate_in_parts = list(map(lambda x : 'gate' in x, message_parts))
    purified_not_in_parts = list(map(lambda x : 'urifie' not in x, message_parts))
    return len(message_parts) >= 8 and any(appeared_in_parts) and any(gate_in_parts) and all(purified_not_in_parts) 
    
def get_monitor(sct):
    selected = None
    monitor_number = 2
    mon = sct.monitors[monitor_number]
    monitor1 = {'top': 285, 'left': 670, 'width': 580, 'height': 35, 'monitor': 1}
    monitor2 = {'top': mon["top"] + 285, 'left': mon["left"] + 680, 'width': 570, 'height': 35, 'monitor': 2}
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
            time.sleep(3)
        cv2.imshow('Image', im)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        time.sleep(1)


        
        
