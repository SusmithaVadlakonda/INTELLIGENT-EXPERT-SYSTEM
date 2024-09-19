import Project1_A05292110main  as M
import json
import logging

# Creating an object
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)


global_problem_value : None
global_conclusion_variable_queue=[]

#ALL THE JSON FILES ARE LOADED HERE
json_file1 = open('Project1-A05292110FORWARD_KNOWLEDGE_BASE.json', "r")
forward_kb_rules = json.load(json_file1)
json_file1.close()
json_file2 = open('Project1-A05292110FORWARD_VARIABLE_LIST.json', "r")
forward_variable_list = json.load(json_file2)
json_file2.close()

#conclusion stack
visited_clause =[]

"""
This function searches the clause number for the goal variable in the caluse variable list 
input: Goal variable
output: clause number
"""   

def search_cvl(goal_variable): #get's the goal variable from the main function
        LOG.info("INSIDE SEARCH_CVL FUCNTION WITH GOAL VARIABLE :%s" % goal_variable)
        clause_num=0
        for key, value in M.FORWARD_CLAUSE_VARIABLE_LIST.items():#check if the goal variable is present in clause_variable list and get the corresponding clause 
            if goal_variable in value and key not in visited_clause:
                clause_num=key
                break     
        LOG.info("visited clause: %s" %visited_clause)
        LOG.info("THIS IS THE CLAUSE NUMBER TO BE PASSED TO NEXT FUNCTION:%s" % clause_num)   
        return clause_num


"""
This function matches each clause variable list elements with symptom variable list and 
takes user input values of the symptoms and updates in variable_list
input: clause number
output:updated variable list 
 
"""   

def update_VL(clause_number:int):
    LOG.info("INSIDE THE UPDATE_VL FUNCTION WITH CLAUSE NUMBER :%s " % clause_number)
    fw_temp_clause_list=M.FORWARD_CLAUSE_VARIABLE_LIST[clause_number] #stores clause variable list corresponding to given clause number
    i=0 # loop variable to run through first index to last index in clause variable list
    visited_clause.append(clause_number)
    for i in range(len(fw_temp_clause_list)): #checking if the variable is instantiated in the variable list or not. If not, it will ask the user to provide the values of variables and instantiate them.  
        if fw_temp_clause_list[i] in forward_variable_list and forward_variable_list[fw_temp_clause_list[i]]["Userinput"]=="":
            while(1):
                        inputvariable = input(forward_variable_list[fw_temp_clause_list[i]]['Question'] +" "+fw_temp_clause_list[i]+"? ")
                        if inputvariable.lower() in  ["yes","no"]:
                            forward_variable_list[fw_temp_clause_list[i]]["Userinput"]  = inputvariable.lower()
                            break
                
            
            M.DERIVED_FORWARD_VARIABLE_LIST[fw_temp_clause_list[i]] = forward_variable_list[fw_temp_clause_list[i]]["Userinput"]
    LOG.info("UPDATING THE FORWARD DERIVED VARIABLE LIST AS :%s "% M.DERIVED_FORWARD_VARIABLE_LIST)
    
    
"""
This function converts clause number to rule number and call validate_Ri with rule number
input:clause number 
output:rule number
"""   
def clause_to_rule(clause_number:int):
    LOG.info("INSIDE THE CLAUSE_TO_RULE FUNCTION WITH CLAUSE NUMBER :%s " % clause_number)
    rule_number = int(clause_number//3)+1
    LOG.info("THIS IS THE CALCULATED RULE NUMBER :%s "% rule_number)
    return rule_number

"""
validate_ri function: validate_ri check the ri rule in kb_rules with user input which is in variable_list.
Once it satisfies the kb rules then it will return corresponding conclusion else it will return None 

FUNCTION VARIABLES
ri : Rule number that we need to validate
conclusion : it is just Null value

FUNCTION RETURNS:
It will return conclusion variable. If the rule is satisfied it will return conclusion in kb_rules
else returns None
"""

def validate_Ri(ri:int):
    LOG.info("INSIDE UPDATE VALIDATE_RULE FUCNTION WITH RULE NUMNER :%s "% ri)
    rule_num = str(ri)
    # A local variable which is created to store the variables used in the rule
    symptoms_list=list(forward_kb_rules[rule_num]['SYMPTOMS'].keys())
    LOG.info("PRINTING THE SYMPTOM PRESENT IN FORWARD KNOWLEGE BASE :%s "% symptoms_list)
    # A flag to track whether the rule is satisfied or not
    flag=0

    # checks each variable in kb rule(ri) with userInput if there is any mismatch loop breaks and returns None
    # else assigns conclusion with conclusion in kb_rule(ri) and then return conclusion
    for symptom in symptoms_list:
        
        if((symptom  in forward_variable_list and forward_kb_rules[rule_num]['SYMPTOMS'][symptom] == forward_variable_list[symptom]['Userinput'])):
            continue
        else:
            #Rule is not satisfied
            flag=1
            break

    if(flag == 0):
        LOG.info("RULE IS SATISFIED AND THE REPAIR RETUREND IS :%s"% forward_kb_rules[rule_num]['REPAIR'])
        global_conclusion_variable_queue.append(forward_kb_rules[rule_num]['REPAIR'])
        return forward_kb_rules[rule_num]['REPAIR']
    LOG.info("This is validate return value:%s"%forward_kb_rules[rule_num]['REPAIR'])
    return None

def process(variable:str):
    LOG.info("INSIDE THE FORWARD PROCESS FUNCTION WITH GLOBAL VARIABLE :%s" % variable)
    while(M.forward_conclusions==None):
        forward_variable_list["PROBLEM"]["Userinput"]=variable
        global_problem_value = "PROBLEM"
        clause_num = search_cvl(global_problem_value)
        update_VL(clause_num)
        rule_num=clause_to_rule(clause_num)
        M.forward_conclusions = validate_Ri(rule_num)
        
    M.DERIVED_FORWARD_VARIABLE_LIST["REPAIR"] = M.forward_conclusions
    json_file = open('Project1-A05292110DERIVED_FORWARD_VARIABLE_LIST.json', "w") 
    #we dump the new dict format into the derived intermediate node JSON file
    json.dump(M.DERIVED_FORWARD_VARIABLE_LIST, json_file, indent=6)
    json_file.close()
    return M.forward_conclusions