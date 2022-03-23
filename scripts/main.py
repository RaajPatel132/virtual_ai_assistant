try:
    import AIAssistant
    import re
    import pprint
    import random
    from configparser import ConfigParser
except Exception as e:
    print("some module are missing{}".format(e))

obj = AIAssistant.AIAssistant()

config_path = 'config/config.ini'
configur = ConfigParser()
configur.read(config_path)
user_name = configur.get('default', 'user_name')

if user_name == '':
    obj.setup(config_path)


def t2s(text):
    obj.text2speech(text)


configur.read(config_path)
user_name = configur.get('default', 'user_name')

t2s("hello " + user_name + ", how can i help you?")

data_path = 'Data/faces/user/'
model_path = 'Data/model/'
face_classifier = 'Data/Haarcascades/haarcascade_frontalface_default.xml'

while True:
    while True:
        res = obj.mic_input()
        print(res)

        if re.search('stop', res):
            obj.shutdown()

        if re.search("dataset create|data set create", res):
            obj.dataset_create(face_classifier, data_path)

        if re.search("train model", res):
            obj.train_model(data_path, model_path)

        if re.search("launch", res):
            dict_app = {
                'chrome': 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                'teamviewer': 'C:\Program Files (x86)\TeamViewer\TeamViewer.exe',
            }

            app = res.split(' ', 1)[1]
            path = dict_app.get(app)
            if path is None:
                t2s('Application path not found')
                print('Application path not found')
            else:
                t2s('Launching: ' + app)
                obj.launchApp(face_classifier, model_path, path)
            break

        if re.search('send email', res):
            config_path = './config/config.ini'
            print(obj.email(config_path))
            break

        if re.search('set up|setup', res):
            obj.setup(config_path)
            break

        if re.search('weather|temperature', res):
            city = res.split(' ')[-1]
            weather_res = obj.weather(city=city)
            print(weather_res)
            t2s(weather_res)
            break

        if re.search('news', res):
            news_res = obj.news()
            type(news_res)
            pprint.pprint(news_res)
            t2s(f"I have found {len(news_res)} news. You can read it. Let me tell you first 2 of them")
            t2s(news_res[0])
            t2s(news_res[1])
            break

        if re.search('tell me about', res):
            topic = res[14:]
            wiki_res = obj.tell_me(topic)
            print(wiki_res)
            t2s(wiki_res)
            break

        if re.search('date', res):
            date = obj.tell_me_date()
            print(date)
            print(t2s(date))
            break

        if re.search('time', res):
            time = obj.tell_me_time()
            print(time)
            t2s(time)
            break

        if re.search('open', res):
            domain = res.split(' ')[-1]
            open_result = obj.website_opener(domain)
            print(open_result)
            break

        if re.search('hello', res):
            print('Hi')
            t2s('Hi')
            break

        if re.search('how are you', res):
            li = ['good', 'fine', 'great']
            response = random.choice(li)
            print(f"I am {response}")
            t2s(f"I am {response}")
            break


        if re.search('what can you do', res):
            li_commands = {
                "open websites": "Example: 'open youtube.com",
                "time": "Example: 'what time it is?'",
                "date": "Example: 'what date it is?'",
                "launch applications": "Example: 'launch chrome'",
                "tell me": "Example: 'tell me about India'",
                "weather": "Example: 'what weather/temperature in Mumbai?'",
                "news": "Example: 'news for today' ",
            }
            ans = """I can do lots of things, for example you can ask me time, date, weather in your city,
            I can open websites for you, launch application and more. See the list of commands-"""
            print(ans)
            pprint.pprint(li_commands)
            t2s(ans)
            break

# hello
# what can you do
# data set create
# train mode
# launch app
# send email
# weather in city
# temperature
# news
# tell me about keyword
# date
# time
# open website
# stop
