## import some modules
from flask import Flask, request, redirect
import twilio.twiml
from yandex_translate import YandexTranslate
from twilio.rest import TwilioRestClient

account_sid = "" #Twilio account sid
auth_token  = "" #Auth token
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST']) ##code to run when a server asks for homepage
def get_message():
    """Main function to forward on translated text"""
    ## Get the body of the text
    body = request.values.get('Body', None)
    print('Full message: ',body)
    ## Get the number of the sms
    senderNumber = request.values.get('From',None)
    ## call the translate function with the body of the text and get the translated text
    message, number = extractMessage(body)
    print('message stripped: ',message)
    print('number is: ',number)
    translated = translate(message)
    print('translated: ',translated)
    sendText(number, translated + ' from ' + senderNumber)
    ## respond with the translated text
    ##resp = twilio.twiml.Response()
    ##resp.message('Your message has been sent')
    ##return str(resp)
    return('Hello')

def extractMessage(message):
    """seperates the number to send to and the message to send"""
    text = message.split()
    number = text[0]
    numberForTwilio = "+44"+number[1:len(number)]
    new_text = message[len(number):len(message)]
    return new_text, numberForTwilio

def translate(text):
    '''Translates the message from one language to another'''
    ## Mr. Scott's secret key for Yandex API
    translate = YandexTranslate('') #Yandex key
    finalText, languageTo = getLanguage(text)
    ## detect the language of the text
    language = translate.detect(finalText)
    print('Translating from',language,'to',languageTo)
    ## translate to english
    translated = 'Translate:', translate.translate(finalText, language+'-'+languageTo)
    return (translated[1]['text'][0])

def sendText(number, message):
    '''Sends the text message to the recipient'''
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body=message,
    to=number,    # Replace with your phone number
    from_="+442033897581") # Replace with your Twilio number 

def getLanguage(message):
    language = message[-2:]
    text = message[0:-2]
    return text, language
## run on port 80
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80,debug=True)
