import requests
from ast import literal_eval

def returnNews():
    result = ""
    url = "http://developer.smartastanaapp.com/OpenApi/api/News/GetAllNews"
    querystring = {"item":"1"}
    headers = {
        'Authorization': "Bearer JCKsjPINZAKFv3aXdNQQejw7KdPYNHwfHoTHJ34Ee62wVUrjf1_PegvEqWwEVi5uuM3o8oBrcCpkgCbGJS-927U4WdY7lcBPr4Oxki9O1BsrQz43QL5LylvYDCRUtLG6MwoO79pbKdgigNyBmFTCFUWralQsxBACrwTjaMXUGXa-8i8cbKDudC1w2Gk2Qo7SU4uCbKqJF8n2LWwPJDhkZJOwIc-XWUiCwx4hmbiiorrkhpi0JHqsrpjieWtSZABlNaHE1K2w7y16gmTC1-Lktxo2xOF62-WCyNarTmk49QK7SN8whm1bltT0fzA33P7L",
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    finalResponse = literal_eval(response.text)
    for news in finalResponse['news']:
        result += (news['subject'])
        result += "\n"
        result += (news['header_photo'])
        result += "\n"

    return result


connect_news = [' ,помимо этого, ', ' ,а также, ', ' ,а из друг новостей, ']


def voiceNews():
    result = ""
    url = "http://developer.smartastanaapp.com/OpenApi/api/News/GetAllNews"
    querystring = {"item":"1"}
    headers = {
        'Authorization': "Bearer JCKsjPINZAKFv3aXdNQQejw7KdPYNHwfHoTHJ34Ee62wVUrjf1_PegvEqWwEVi5uuM3o8oBrcCpkgCbGJS-927U4WdY7lcBPr4Oxki9O1BsrQz43QL5LylvYDCRUtLG6MwoO79pbKdgigNyBmFTCFUWralQsxBACrwTjaMXUGXa-8i8cbKDudC1w2Gk2Qo7SU4uCbKqJF8n2LWwPJDhkZJOwIc-XWUiCwx4hmbiiorrkhpi0JHqsrpjieWtSZABlNaHE1K2w7y16gmTC1-Lktxo2xOF62-WCyNarTmk49QK7SN8whm1bltT0fzA33P7L",
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    finalResponse = literal_eval(response.text)
    i = 0
    for news in finalResponse['news']:

        result += (news['subject'])
        if(i != 2):
            result += connect_news[i]
        i = i + 1
        if(i == 3):
            break

    return result
