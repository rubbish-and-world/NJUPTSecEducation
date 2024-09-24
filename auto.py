import json as j
import requests as r

# This json is for '准入资格C类', if you have a different course, get your own json file from http://10.xxx.xxx.xxx:9092/students/courseList

# get course IDs
f = open("courseList.json" ,"rt" , encoding='utf-8')
allCourse = j.load(f)
IDs =  []
for lecture in allCourse:
    IDs.extend([x["id"] for x in lecture['result']])
f.close()


url = "http://10.xxx.xxx.xxx:9090/jeecg-boot/jcedutec/courseSource/finish"

questionURL = "http://10.xxx.xxx.xxx:9090/jeecg-boot/jcedutec/courseSource/queryCourseQuestionRelaByMainId?id="

submitURL = "http://10.xxx.xxx.xxx:9090/jeecg-boot/jcedutec/courseSource/submitAnswer"

headers = {
"Accept":"application/json, text/plain, */*",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"en,zh-CN;q=0.9,zh;q=0.8",
"Origin":"http://10.xxx.xxx.xxx:9092",
"Referer":"http://10.xxx.xxx.xxx:9092/",
"X-Access-Token":"===========================================", # Fill your own token here
"X-Sign":"==================================================", # Fill your own sign here
"X-TIMESTAMP":"1727160689408", # Fill your own timestamp (optional)
"tenant-id":"0",
"ContentType" : "application/json;charset=UTF-8"
}




class questinAnswer():
    def __init__(self, questionID , videoID , options) -> None:
        self.questionID = questionID
        self.videoID = videoID
        self.options = options

    def __str__(self) -> str:
        return f"[{self.questionID=}|{self.videoID=}|{self.options=}]"


def getQuestionList(id) -> list: # return list of questionAnswers
    res = []
    resp = r.get(questionURL + id, headers=headers)
    onError(resp)
    received = j.loads(resp.content.decode('utf-8'))
    questionList =  received['result']
    if questionList:
        for question in questionList:
            res.append(questinAnswer(question['id'] , question['courseId'] , question['correctAnswer'] if len(question['correctAnswer'])==1 else question['correctAnswer'].split()) )
    return res

    

def onError(resp):
    if resp.status_code != 200:
        print("Error on : " , id)    


def sendWatch(id):
    payload = {
        "id" : id
    }
    resp = r.post(url , headers=headers , json=payload)
    print(resp.text)
    onError(resp)

def submit(ans):
    payload = {
        'id' : ans.videoID ,
        'option' : ans.options,
        'questionId' : ans.questionID ,
    }
    print(payload)
    resp = r.post(submitURL , headers=headers , json=payload)
    print(resp.text)
    onError(resp)

for index , id in enumerate(IDs):
    sendWatch(id)
    ansList = getQuestionList(id)
    if ansList:
        for ans in ansList:
            print(index , end=' :')
            submit(ans)

print('Done')
