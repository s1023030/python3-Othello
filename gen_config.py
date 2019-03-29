# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 19:32:03 2019

@author: GATL
"""
import configparser 
  
cf = configparser.ConfigParser()
cf.add_section('AI')
cf.set('AI',"0",'Random')
cf.write(open("Othello.cfg","w"))
