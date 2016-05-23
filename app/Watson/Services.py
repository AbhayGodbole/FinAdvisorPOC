"""
    Module will contain all Watson Service APIs 
    Different funtions to handle various Services
"""

""" Using AlchemyLanguage Service """
 
import json, requests
from watson_developer_cloud import AlchemyLanguageV1
from watson_developer_cloud import AlchemyDataNewsV1

def AlchemyLanguageText(text,inputType):
    alchemy_language = AlchemyLanguageV1(api_key="6986aa6422f93320f04afb2fc73b185d1f64f16c")
    combined_operations = ['page-image', 'entity', 'keyword', 'title', 'author', 'taxonomy', 'concept', 'doc-emotion']
    #response = json.dumps(alchemy_language.combined(text=text, extract=combined_operations), indent=2)
    if inputType == "Text" :
        response = json.dumps(alchemy_language.combined(text=text, extract=combined_operations), indent=2)
    elif inputType == "Url" :
        response = json.dumps(alchemy_language.combined(url=text, extract=combined_operations), indent=2)
    else :
        response = json.dumps(alchemy_language.combined(html=text, extract=combined_operations), indent=2)
    
    return response

def getKeywords(response):
    json_string = json.loads(response)
    return  json_string['keywords']

def getConcepts(response):
    json_string = json.loads(response)
    return json_string['concepts']

def AlchemyDataNewsConcept( concepts):
    """var1 = json.dumps(concepts)
    print(isinstance(var1, dict))
    print("Concepts: ", json.dumps(concepts))
    alchemy_data_news = AlchemyDataNewsV1(api_key="6986aa6422f93320f04afb2fc73b185d1f64f16c")
    results = alchemy_data_news.get_news_documents(
                                                                            start='now-7d',
                                                                             end='now' ,
                                                                            return_fields=['enriched.url.title',
                                                                           'enriched.url.url',
                                                                           'enriched.url.author',
                                                                           'enriched.url.publicationDate'],
                                                                           #query_fields={json.dumps(concepts), json.dumps(keywords)}
                                                                            query_fields={'q.enriched.url.concepts': ['Apple Store','IBM']}
                                                                           )"""
    Concept = ''
    for concept in concepts :
        relevance = round(float(concept['relevance']) * 100)
        if relevance > 60 :
            Concept=  Concept +  concept['text'].replace(" ","%20")
            Concept = Concept + "^"
    
    Concept = "[" + Concept[:len(Concept) - 1]  + "]"       
    url = 'https://gateway-a.watsonplatform.net/calls/data/GetNews?outputMode=json&start=now-1d&end=now&count=10&q.enriched.url.concepts.concept.text=' + Concept + '&return=enriched.url.url,enriched.url.title&apikey=6986aa6422f93320f04afb2fc73b185d1f64f16c'
    print(url)
    resultConcept = requests.get(url)
    return resultConcept.text
   # return  json.dumps(resultConcept.text, indent=2)
    
def AlchemyDataNewsKeyword( keywords):
    Keyword = ''
    for keyword in keywords :
        relevance = round(float(keyword['relevance']) * 100)
        if relevance > 60 :
            Keyword=  Keyword +  keyword['text'].replace(" ","%20")
            Keyword = Keyword + "^"
    
    Keyword = "[" + Keyword[:len(Keyword) - 1]  + "]"       
    url = 'https://gateway-a.watsonplatform.net/calls/data/GetNews?outputMode=json&start=now-1d&end=now&count=10&q.enriched.url.keywords.keyword.text=' + Keyword + '&return=enriched.url.url,enriched.url.title&apikey=6986aa6422f93320f04afb2fc73b185d1f64f16c'
    print(url)
    resultKeyword =  requests.get(url)
    return resultKeyword.text
    # return  json.dumps(resultKeyword.text, indent=2)  # + "\n" + json.dumps(resultKeyword.text, indent=2)