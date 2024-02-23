import warnings
warnings.filterwarnings("ignore")

import re
from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta

__all__ = ['clean_text', 'strip_str_datetime']


def strip_str_datetime(date_str1, date_str2):
    if date_str1=="None" or date_str2=="None":
        return None
    return (parser.parse(date_str1) - parser.parse(date_str2)).days

def clean_text(text):

    text = re.sub("\r\n", "\n", text)
    text = re.sub(r"[.]+", ".", text)
    text = re.sub(r" +", " ", text)
    
    text = re.sub(",\n", ",", text)
    text = re.sub(", \n", ", ", text)
    text = re.sub(";\n", ";", text)
    text = re.sub("; \n", "; ", text)
    text = re.sub("'\n",  "'", text)
    text = re.sub("' \n", "' ", text)
    text = re.sub("\"\n",  "\"", text)
    text = re.sub("\" \n", "\" ", text)
    text = re.sub("-\n",  "-", text)
    text = re.sub("- \n", "- ", text)

    text = re.sub("\n:", ":", text)
    text = re.sub("\n :", ":", text)
    text = re.sub("\n,", ",", text)
    text = re.sub("\n ,", ",", text)
    text = re.sub("\n;", ";", text)
    text = re.sub("\n ;", ";", text)
    text = re.sub("\n'",  "'", text)
    text = re.sub("\n '", "'", text)
    text = re.sub("\n (", " (", text)
    text = re.sub("\n(", "(", text)
    
    repl = re.findall(r"\n[a-z]", text)
    for r in repl:
        text = re.sub(r, ' '+r[-1], text)   
        
    repl = re.findall(r"\n [a-z]", text)
    for r in repl:
        text = re.sub(r, ' '+r[-1], text)   
            
    text = re.sub("\n.", ".", text)
        
    text = re.sub("..", '.', text)
    text = re.sub("--", '-', text)
    text = re.sub("==", '=', text)
    text = re.sub("**", '*', text)
    text = re.sub("\s+", " ", text)
    
    text = text.replace("10- CM", "10-CM")
    text = text.replace("ICD- 10", "ICD-10")
    text = text.replace("ICD-10-CM \nF", "ICD-10-CM F")
    text = text.replace(",uncomplicated", ", uncomplicated")
    text = text.replace("Use \nDisorder", "Use Disorder")
    text = text.replace("\nUse Disorder", "Use Disorder")
    text = text.replace(" \nDependence", " Dependence")
    text = text.replace("*\n NO", "* NO")
    text = text.replace("in sustained \nRemission", "in sustained Remission")
    text = text.replace("\n On Maintenance Therapy", " On Maintenance Therapy")
    text = text.replace("On \nMaintenance Therapy", "On Maintenance Therapy")
    
    return text
