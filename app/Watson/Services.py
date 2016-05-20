"""
    Module will contain all Watson Service APIs 
    Different funtions to handle various Services
"""

""" Using AlchemyLanguage Service """
 
import json
from watson_developer_cloud import AlchemyLanguageV1

def AlchemyLanguageText(text):
    alchemy_language = AlchemyLanguageV1(api_key="6986aa6422f93320f04afb2fc73b185d1f64f16c")
    combined_operations = ['page-image', 'entity', 'keyword', 'title', 'author', 'taxonomy', 'concept', 'doc-emotion']
    response = json.dumps(alchemy_language.combined(text=text, extract=combined_operations), indent=2)
    
    return response