def get_prompt(prompt_desc):
    '''
    Helper function to generate prompts
    '''    
    prompt = None
    if prompt_desc == 'alcohol': prompt = f"""\
Extract the reference to alcohol use disorder diagnosis \
with surrounding information relevant to it \
from the diagnoses section in the following note. \
If you can\'t find the answer, please respond "unanswerable". \n note: """

    elif prompt_desc == 'opioid': prompt = f"""\
Extract the reference to opioid or heroin use disorder diagnosis \
with surrounding information relevant to it \
from the diagnoses section in the following note. \
If you can\'t find the answer, please respond "unanswerable". \n note: """

    elif prompt_desc == 'cannabis': prompt = f"""\
Extract the reference to cannabis use disorder diagnosis \
with surrounding information relevant to it \
from the diagnoses section in the following note. \
If you can\'t find the answer, please respond "unanswerable". \n note: """

    elif prompt_desc == 'amphetamine': prompt = f"""\
Extract the reference to the use disorder diagnosis of stimulant such as amphetamine or methamphetamine \
with surrounding information relevant to it \
from the diagnoses section in the following note. \
If you can\'t find the answer, please respond "unanswerable". \n note: """
        
    elif prompt_desc == 'cocaine': prompt = f"""\
Extract the reference to the use disorder diagnosis of stimulant such as cocaine \
with surrounding information relevant to it \
from the diagnoses section in the following note. \
If you can\'t find the answer, please respond "unanswerable". \n note: """
        
    elif prompt_desc == 'nicotine': prompt = f"""\
Extract the reference to nicotine use disorder diagnosis \
with surrounding information relevant to it \
from the diagnoses section in the following note. \
If you can\'t find the answer, please respond "unanswerable". \n note: """
        
    elif prompt_desc == 'hallucinogen': prompt = f"""\
Extract the reference to hallucinogen or hallucinogenic use disorder diagnosis \
with surrounding information relevant to it \
from the diagnoses section in the following note. \
If you can\'t find the answer, please respond "unanswerable". \n note: """
        
    elif prompt_desc == 'caffeine': prompt = f"""\
Extract the reference to caffeine use disorder diagnosis \
with surrounding information relevant to it \
from the diagnoses section in the following note. \
If you can\'t find the answer, please respond "unanswerable". \n note: """
        
    elif prompt_desc == 'inhalant': prompt = f"""\
Extract the mention of inhalant dependence \
with surrounding information relevant to it \
from the diagnoses section in the following note. \
If you can\'t find the answer, please respond "unanswerable". \n note: """
        
    elif prompt_desc == 'other psychoactive': prompt = f"""\
Extract the mention of other psychoactive substance dependence \
with surrounding information relevant to it \
from the diagnoses section in the following note. \
If you can\'t find the answer, please respond "unanswerable". \n note: """
        
    elif prompt_desc == 'sedative, hypnotic, or anxiolytic': prompt = f"""\
Extract the reference to sedative, hypnotic, or anxiolytic use disorder diagnosis \
with surrounding information relevant to it \
from the diagnoses section in the following note. \
If you can\'t find the answer, please respond "unanswerable". \n note: """
    else:
        raise NotImplementedError

    return prompt

