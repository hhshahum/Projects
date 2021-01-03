#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#This is the work done by Harshal Shah(1020849) and Kamakshi Banavalikar(1039197)

# This Python file uses the following encoding: utf-8

#Import all the libraries
import json
from collections import Counter
from mpi4py import MPI
import time
import re
import operator

#Declare/Initialize all the variables and data structures 
start=time.time()
comm=MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
splitarray=[[]for i in range(size)]
hashtag=[]
hashtaglan=[]
hasharray=[]
lanarray=[]

#ISO 639-1 List of languages
lang_code = {'ab':'Abkhazian'
,'aa':'Afar'
,'af':'Afrikaans'
,'ak':'Akan'
,'sq':'Albanian'
,'am':'Amharic'
,'ar':'Arabic'
,'an':'Aragonese'
,'hy':'Armenian'
,'as':'Assamese'
,'av':'Avaric'
,'ae':'Avestan'
,'ay':'Aymara'
,'az':'Azerbaijani'
,'bm':'Bambara'
,'ba':'Bashkir'
,'eu':'Basque'
,'be':'Belarusian'
,'bn':'Bengali'
,'bh':'Bihari'
,'bi':'Bislama'
,'bs':'Bosnian'
,'br':'Breton'
,'bg':'Bulgarian'
,'my':'Burmese'
,'ca':'Catalan'
,'ch':'Chamorro'
,'ce':'Chechen'
,'ny':'Chichewa'
,'zh':'Chinese'
,'cv':'Chuvash'
,'kw':'Cornish'
,'co':'Corsican'
,'cr':'Cree'
,'hr':'Croatian'
,'cs':'Czech'
,'da':'Danish'
,'dv':'Divehi'
,'nl':'Dutch'
,'dz':'Dzongkha'
,'en':'English'
,'eo':'Esperanto'
,'et':'Estonian'
,'ee':'Ewe'
,'fo':'Faroese'
,'fj':'Fijian'
,'fi':'Finnish'
,'fr':'French'
,'ff':'Fulah'
,'gl':'Galician'
,'ka':'Georgian'
,'de':'German'
,'el':'Greek'
,'gn':'Guarani'
,'gu':'Gujarati'
,'ht':'Haitian'
,'ha':'Hausa'
,'he':'Hebrew'
,'hz':'Herero'
,'hi':'Hindi'
,'ho':'Hiri Motu'
,'hu':'Hungarian'
,'ia':'Interlingua'
,'id':'Indonesian'
,'ie':'Interlingue'
,'ga':'Irish'
,'ig':'Igbo'
,'ik':'Inupiaq'
,'io':'Ido'
,'is':'Icelandic'
,'it':'Italian'
,'iu':'Inuktitut'
,'ja':'Japanese'
,'jv':'Javanese'
,'kl':'Kalaallisut'
,'kn':'Kannada'
,'kr':'Kanuri'
,'ks':'Kashmiri'
,'kk':'Kazakh'
,'km':'Central Khmer'
,'ki':'Kikuyu'
,'rw':'Kinyarwanda'
,'ky':'Kirghiz'
,'kv':'Komi'
,'kg':'Kongo'
,'ko':'Korean'
,'ku':'Kurdish'
,'kj':'Kuanyama'
,'la':'Latin'
,'lb':'Luxembourgish'
,'lg':'Ganda'
,'li':'Limburgan'
,'ln':'Lingala'
,'lo':'Lao'
,'lt':'Lithuanian'
,'lu':'Luba-Katanga'
,'lv':'Latvian'
,'gv':'Manx'
,'mk':'Macedonian'
,'mg':'Malagasy'
,'ms':'Malay'
,'ml':'Malayalam'
,'mt':'Maltese'
,'mi':'Maori'
,'mr':'Marathi'
,'mh':'Marshallese'
,'mn':'Mongolian'
,'na':'Nauru'
,'nv':'Navajo'
,'nd':'North Ndebele'
,'ne':'Nepali'
,'ng':'Ndonga'
,'nb':'Norwegian Bokmal'
,'nn':'Norwegian Nynorsk'
,'no':'Norwegian'
,'ii':'Sichuan Yi'
,'nr':'South Ndebele'
,'oc':'Occitan'
,'oj':'Ojibwa'
,'cu':'Church Slavic'
,'om':'Oromo'
,'or':'Oriya'
,'os':'Ossetian'
,'pa':'Punjabi'
,'pi':'Pali'
,'fa':'Persian'
,'pl':'Polish'
,'ps':'Pashto'
,'pt':'Portuguese'
,'qu':'Quechua'
,'rm':'Romansh'
,'rn':'Rundi'
,'ro':'Romanian'
,'ru':'Russian'
,'sa':'Sanskrit'
,'sc':'Sardinian'
,'sd':'Sindhi'
,'se':'Northern Sami'
,'sm':'Samoan'
,'sg':'Sango'
,'sr':'Serbian'
,'gd':'Gaelic'
,'sn':'Shona'
,'si':'Sinhala'
,'sk':'Slovak'
,'sl':'Slovenian'
,'so':'Somali'
,'st':'Southern Sotho'
,'es':'Spanish'
,'su':'Sundanese'
,'sw':'Swahili'
,'ss':'Swati'
,'sv':'Swedish'
,'ta':'Tamil'
,'te':'Telugu'
,'tg':'Tajik'
,'th':'Thai'
,'ti':'Tigrinya'
,'bo':'Tibetan'
,'tk':'Turkmen'
,'tl':'Tagalog'
,'tn':'Tswana'
,'to':'Tonga'
,'tr':'Turkish'
,'ts':'Tsonga'
,'tt':'Tatar'
,'tw':'Twi'
,'ty':'Tahitian'
,'ug':'Uighur'
,'uk':'Ukrainian'
,'ur':'Urdu'
,'uz':'Uzbek'
,'ve':'Venda'
,'vi':'Vietnamese'
,'vo':'Volapuk'
,'wa':'Walloon'
,'cy':'Welsh'
,'wo':'Wolof'
,'fy':'Western Frisian'
,'xh':'Xhosa'
,'yi':'Yiddish'
,'yo':'Yoruba'
,'za':'Zhuang'
,'zu':'Zulu'
,'und':'Undefined'}


#Converting tuple to dictionary
def Convert(tup, di):
    di = dict(tup)
    return di

#Renaming keys of dictionary
def rename_keys(d, keys):
    return dict([(keys.get(k,k), v) for k, v in d.items()])

#Checking for english and non english characters in the string
def checkEnglish(mystring):
    try:
        mystring.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
   
##Identifying the hashtags and the lanaguages used for tweeting
def calculate_tweets(data):
    text = data["doc"]["text"].split(" ")
    lang = data["doc"]["metadata"]["iso_language_code"]
    for tweet in range(len(text)):
        if((text[tweet].startswith("#")) and not (bool(re.search("[!$%^&'-*+.|<>]|^[0-9]", re.sub("[.$]",'',text[tweet]))))):      #Checking for valid hashtags
           newstring = text[tweet]
           newstring = newstring.lower()            #Converting string to lower case
           newstring = re.sub('[.$]','',newstring)  #Checking for charcters at the last
           retval = checkEnglish(newstring)         #Output from the function checking english and non english characters
           if((len(newstring)>1) and retval==True and not(newstring[1:].isdigit())): #If valid hashtag and english characters used then append hashtag and lanaguage used, else append only the lanaguage used
               hashtag.append(newstring)
               hashtaglan.append(lang.lower())
           else:
               hashtaglan.append(lang.lower())
     
    return hashtag,hashtaglan
               
#Reading the file and parsing it line by line
with open('bigTwitter.json') as atweet:
    i=0
    for line in atweet:
        if(i%size)==rank:       #Assigning the single tweet to the processor based on its rank
            try:
                line = line.replace(",\n","")           #Resolving the json formatting error
                tweet=json.loads(line)
                joinarray = calculate_tweets(tweet)         #Getting the valid hashtags and language for that tweet
            except:
                pass
        i+=1

joinarray=comm.gather(joinarray,root=0)         #Gather the results from all the processors

#The master process creates two different lists for hashtags and languages
if rank==0:
    for i in range(size):
        for j in range(2):
            if j==0:
                hasharray.append(joinarray[i][j])
            elif j==1:
                lanarray.append(joinarray[i][j])
    
    #Final Hashtag List
    finalhasharray = []
    for sublist in hasharray:
        for item in sublist:
            finalhasharray.append(item)
    
    #Final Language List
    finallanarray = []
    for sublist in lanarray:
        for item in sublist:
            finallanarray.append(item)
            
    #Converting the tuples to dictionaries and renaming keys for clear and precise outputs
    HashCountDict = Convert(Counter(finalhasharray).most_common(10),{})
    LangCodeCountDict = Convert(Counter(finallanarray).most_common(10), {})
    FullFormLangCount = rename_keys(LangCodeCountDict, lang_code)
   
    #Top 10 Hashtags (sorted in descending order)
    print("Top 10 hashtags with its count ...")
    cnt=0
    for key,value in sorted(HashCountDict.items(),key=operator.itemgetter(1),reverse=True):
        cnt+=1
        print(cnt,"->",key,":",value)
   
    print("\n")
    
    #Top langauges used for tweeting (sorted in descending order)
    print("Top 10 Languages with its count ...")
    cnt=0
    for key,value in sorted(FullFormLangCount.items(),key=operator.itemgetter(1),reverse=True):
        cnt+=1
        print(cnt,"->",key,":",value)

    end=time.time()
    (hours,rem) = divmod(end-start,3600)
    (minutes,seconds) = divmod(rem,60)
    
    #Calculating the final time taken for execution
    print('\nTime Elapsed :', '{:0>2}:{:0>2}:{:05.2f}'.format(int(hours), int(minutes), seconds))