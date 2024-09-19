import Project1_A05292110main as M
import json
import logging


# Creating an object
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)


#READING AND LOADING ALL THE NECESSARY JSON FILES NEEDED FOR PROCESSING
json_file1 = open('Project1-A05292110BACKWARD_KNOWLEDGE_BASE.json', "r")
kb_rules = json.load(json_file1)
json_file2 = open('Project1-A05292110BACKWARD_VARIABLE_LIST.json', "r")
variable_list = json.load(json_file2)  
json_file3 = open('Project1-A05292110BACKWARD_INTERMEDIATE_NODE.json', "r")
intermediate_node = json.load(json_file3)  
json_file1.close() 
json_file2.close()
json_file3.close()

#conclusion stack
visited_rules=[]
"""
This function searches the rule number for the goal variable in the conclusion list 
input: Goal variable
output: rule number
"""    

def search_con(goal_variable):
    LOG.info("INSIDE SEARCH_CON FUCNTION WITH GOAL VARIABLE :%s" % goal_variable)
    rule_num=1
    for ri,con in M.CONCLUSION_LIST.items():#check if the goal variable is present in conclusion list and get the corresponding rules into the clause_num_list
        if(con==goal_variable and ri not in visited_rules):
            rule_num=ri
            break
    LOG.info("visited rules: %s" %visited_rules)
    LOG.info("THIS IS THE RULE TO BE PASSED TO NEXT FUNCTION:%s" % rule_num)
    return rule_num
        

"""
This function converts rule number to clause number 
input:rule number 
output:clause number
"""    
def rule_to_clause(rule_number:int):
    LOG.info("INSIDE THE RULE_TO_CLAUSE FUNCTION WITH RULE NUMBER :%s " % rule_number)
    clause_number=10*(rule_number-1)+1
    LOG.info("THIS IS THE CALCULATED CLAUSE NUMBER :%s "% clause_number)
    return clause_number
       

"""
This function matches each clause variable list elements with symptom variable list and 
takes user input values of the symptoms and updates in variable_list
input: clause number
output:updated variable list 
 
"""   
def update_VL(clause_number:int):
    LOG.info("INSIDE UPDATE VL FUNCTION AT WITH CLAUSE NUMBER :%s "% clause_number)
    temp_clause_list = M.CLAUSE_VARIABLE_LIST[clause_number]
    
    for clause_var in temp_clause_list:
        if clause_var in intermediate_node.keys() and intermediate_node[clause_var]['Userinput'] == "":
            process(clause_var) 

    for i in range(len(temp_clause_list)):  
        if temp_clause_list[i] in intermediate_node.keys() and intermediate_node[temp_clause_list[i]]['Userinput'] == "no":
            return "done"      
        if temp_clause_list[i] in variable_list:
            if variable_list[temp_clause_list[i]]['Userinput'] == "":
                while True:
                    inputvariable = input(variable_list[temp_clause_list[i]]["Question"] + " (YES/NO): ")
                    if inputvariable.lower() in ["yes", "no"]:
                        variable_list[temp_clause_list[i]]['Userinput'] = inputvariable.lower()
                        break
                    else:
                        print("Please respond with YES or NO.")
                M.DERIVED_VARIABLE_LIST[temp_clause_list[i]] = variable_list[temp_clause_list[i]]['Userinput']
    
    LOG.info("UPDATING THE DERIVED VARIABLE LIST AS :%s "% M.DERIVED_VARIABLE_LIST)
    return "done"

# def update_VL(clause_number:int):
#     LOG.info("INSIDE UPDATE VL FUNCTION AT WITH CLAUSE NUMBER :%s "% clause_number)
#     #stores clause variable list corresponding to given clause number
#     temp_clause_list=M.CLAUSE_VARIABLE_LIST[clause_number]
#     for clause_var in temp_clause_list:
#         if(clause_var in intermediate_node.keys() ):
#             if(intermediate_node[clause_var]['Userinput']==""):
#                 process(clause_var) 
#     for i in range(len(temp_clause_list)):  
#             if(temp_clause_list[i] in intermediate_node.keys() and intermediate_node[temp_clause_list[i]]['Userinput']=="no"):
#                 return "done"      
#             if temp_clause_list[i] in variable_list:
#                 if(variable_list[temp_clause_list[i]]['Userinput']==""):
#                     while(1):
#                         inputvariable = input(variable_list[temp_clause_list[i]]["Question"]+""+temp_clause_list[i]+"? ")
#                         if inputvariable.lower() in  ["yes","no"]:
#                             variable_list[temp_clause_list[i]]['Userinput'] = inputvariable.lower()
#                             break
#                     M.DERIVED_VARIABLE_LIST[temp_clause_list[i]] = variable_list[temp_clause_list[i]]['Userinput']   
#     LOG.info("UPDATING THE DERIVED VARIABLE LIST AS :%s "% M.DERIVED_VARIABLE_LIST)
#     return "done"


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

# def validate_ri(ri:int,conclusion:str):
#     LOG.info("INSIDE UPDATE VALIDATE_RULE FUCNTION WITH RULE NUMNER :%s "% ri)
#     rule_num = str(ri)
#     # A local variable which is created to store the variables used in the rule
#     symptoms_list=list(kb_rules[rule_num]['SYMPTOMS'].keys())
#     LOG.info("PRINTING THE SYMPTOM PRESENT IN KNOWLEGE BASE :%s "% symptoms_list)
#     # A flag to track whether the rule is satisfied or not
#     flag=0
#     visited_rules.append(ri)
#     # checks each variable in kb rule(ri) with userInput if there is any mismatch loop breaks and returns None
#     # else assigns conclusion with conclusion in kb_rule(ri) and then return conclusion
#     for symptom in symptoms_list:
#         if((symptom  in variable_list and kb_rules[rule_num]['SYMPTOMS'][symptom] == variable_list[symptom]['Userinput'])
#           or (symptom in intermediate_node and kb_rules[rule_num]['SYMPTOMS'][symptom] == intermediate_node[symptom]['Userinput'])):
#             #print(symptom)
#             continue
#         else:
#             #print(symptom)
#             #Rule is not satisfied
#             flag=1
#             break
#     # flag =0 means the rule(ri) is satisfied and returns the conclusion
#     if(flag == 0):
#         conclusion=kb_rules[rule_num]['CONCLUSION']
#         LOG.info("RULE IS SATISFIED AND THE CONCLUSION RETUREND IS :%s"% conclusion)
#         if(conclusion in intermediate_node.keys()):
#             intermediate_node[conclusion]["Userinput"]="yes"
#             M.DERIVED_VARIABLE_LIST[conclusion]=intermediate_node[conclusion]["Userinput"]
#     else:
#         if(kb_rules[rule_num]['CONCLUSION'] in intermediate_node.keys()):
#             intermediate_node[kb_rules[rule_num]['CONCLUSION']]["Userinput"]="no"
#             M.DERIVED_VARIABLE_LIST[kb_rules[rule_num]['CONCLUSION']]=intermediate_node[kb_rules[rule_num]['CONCLUSION']]["Userinput"]
#     LOG.info("This is validate return value:%s"%conclusion)
#     return conclusion
def validate_ri(ri:int, conclusion:str):
    LOG.info("INSIDE VALIDATE_RULE FUNCTION WITH RULE NUMBER :%s", ri)
    rule_num = str(ri)
    symptoms_list = list(kb_rules[rule_num]['SYMPTOMS'].keys())
    LOG.info("Symptoms present in knowledge base: %s", symptoms_list)
    flag = 0
    visited_rules.append(ri)

    for symptom in symptoms_list:
        if ((symptom in variable_list and kb_rules[rule_num]['SYMPTOMS'][symptom] == variable_list[symptom]['Userinput']) or
            (symptom in intermediate_node and kb_rules[rule_num]['SYMPTOMS'][symptom] == intermediate_node[symptom]['Userinput'])):
            continue
        else:
            flag = 1
            break

    if flag == 0:
        conclusion = kb_rules[rule_num]['CONCLUSION']
        LOG.info("Rule satisfied, conclusion: %s", conclusion)
        # Update the derived variable list
        M.DERIVED_VARIABLE_LIST["PROBLEM"] = conclusion
        return conclusion
    else:
        return None  # Ensure it returns None if not satisfied

    

# def process(goal):
#     LOG.info("INSIDE THE PROCESS FUNCTION WITH GLOBAL VARIABLE :%s" % goal)
    
#     while((goal in intermediate_node.keys() and intermediate_node[goal]["Userinput"]=="") or 
#      (goal not in intermediate_node.keys() and  M.backward_conclusions not in M.PROBLEM_LIST and M.backward_conclusions != "NO PROBLEM")):
#         rule_num = search_con(goal)
#         clause_num = rule_to_clause(rule_num)
#         d = update_VL(clause_num) 
#         M.backward_conclusions = validate_ri(rule_num,M.backward_conclusions)
#         if intermediate_node["ENGINE PROBLEM"]["Userinput"] == "no":
#             break
#         flag1=0
#         for key in intermediate_node.keys():
#             if intermediate_node[key]["Userinput"]=="":
#                 flag1=1  
#                 break
#         if flag1==0:
#             break
  
#     LOG.info("YOUR VALUE IS :%s" % M.backward_conclusions)
    
#     M.DERIVED_VARIABLE_LIST["PROBLEM"] = M.backward_conclusions
#     json_file = open('Project1-A05292110DERIVED_BACKWARD_VARIABLE_LIST.json', "w") 
#     #we dump the new dict format into the derived intermediate node JSON file
#     json.dump(M.DERIVED_VARIABLE_LIST, json_file, indent=6)
#     json_file.close()
#     #print("You are suffering from " , M.conclusions)
#     return M.backward_conclusions

def process(goal):
    LOG.info("INSIDE THE PROCESS FUNCTION WITH GOAL VARIABLE :%s" % goal)
    
    while True:
        rule_num = search_con(goal)
        if rule_num is None:
            break  # No more rules to process
        clause_num = rule_to_clause(rule_num)
        d = update_VL(clause_num)
        
        if d == "done":  # Only break if done updating
            break
        
        M.backward_conclusions = validate_ri(rule_num, M.backward_conclusions)
        
        if M.backward_conclusions in ["NO PROBLEM", "ENGINE PROBLEM", "OTHER_CONCLUSIONS"]:  # Adjust as needed
            break  # Exit when a conclusion is reached

    LOG.info("Final conclusion: %s", M.backward_conclusions)
    return M.backward_conclusions



