#This file contains the declaration and initilaization of variables
import logging
import Project1_A05292110Problem_BW as BW
import Project1_A05292110Repair_FW as FW
import time
import psutil

CONCLUSION_LIST = {
    1: "NO PROBLEM",
    2: "ELECTRICAL SYSTEM PROBLEM",
    3: "STARTER PROBLEM",
    4: "BATTERY PROBLEM",
    5: "POWER STEERING PUMP FAILURE",
    6: "ENGINE PROBLEM",
    7: "COOLANT LEAK",
    8: "RADIATOR FAN MALFUNCTION",
    9: "ENGINE MISFIRE",
    10: "LOW FUEL PRESSURE",
    11: "AIR INTAKE SYSTEM PROBLEM",
    12: "TRANSMISSION PROBLEM",
    13: "TRANSMISSION FLUID PROBLEM",
    14: "TRANSMISSION SLIPPAGE PROBLEM",
    15: "DAMAGED TRANSMISSION MOUNTS",
    16: "TRANSMISSION FLUID LEAK",
    17: "BRAKE SYSTEM PROBLEM",
    18: "LOW BRAKE FLUID",
    19: "AIR IN BRAKE LINES",
    20: "VACUUM SYSTEM ISSUE",
    21: "WORN BRAKE PADS ISSUE",
    22: "STEERING/SUSPENSION PROBLEM",
    23: "WARPED BRAKE ROTORS",
    24: "UNBALANCED TIRES",
    25: "LOW POWER STEERING FLUID",
    26: "BINDING STEERING COMPONENTS",
    27: "WORN CV JOINTS",
    28: "LOOSE OR BROKEN HEAT SHIELD",
    29: "EXHAUST LEAK",
    30: "EXCESSIVE SMOKE FROM EXHAUST"
}


#CLAUSE_VARIABLE_LIST is a variable of dict with list datastructure that contains the clause number as key and thge corresponding symptoms list
CLAUSE_VARIABLE_LIST = {
    1:  ["CAR GOT PROBLEM", "NO"],  # Rule 1
    11: ["CAR IS HAVING DIFFICULTY", "YES", "DASHBOARD LIGHTS DIM WHEN CAR STARTS", "YES"],  # Rule 2
    21: ["CAR IS HAVING DIFFICULTY", "YES", "DASHBOARD LIGHTS DIM WHEN CAR STARTS", "NO", "CAR MAKES CLICKING SOUND WHEN KEY IS TURNED", "YES", "CAR HAS POWER", "YES"],  # Rule 3
    31: ["CAR IS HAVING DIFFICULTY", "YES", "DASHBOARD LIGHTS DIM WHEN CAR STARTS", "NO", "CAR MAKES CLICKING SOUND WHEN KEY IS TURNED", "YES", "CAR HAS POWER", "NO"],  # Rule 4
    41: ["CAR IS HAVING DIFFICULTY", "YES", "DASHBOARD LIGHTS DIM WHEN CAR STARTS", "NO", "CAR MAKES CLICKING SOUND WHEN KEY IS TURNED", "NO", "STEERING WHEEL STIFF", "YES", "NOISE WHEN TURNING", "YES"],  # Rule 5
    51: ["CAR IS HAVING DIFFICULTY", "NO", "POOR ACCELERATION", "YES", "NOISE FROM ENGINE", "YES", "ENGINE LIGHT ON", "YES"],  # Rule 6
    61: ["ENGINE PROBLEM", "YES", "ENGINE OVERHEATING", "YES", "COOLANT LEVEL LOW", "YES"],  # Rule 7
    71: ["ENGINE PROBLEM", "YES", "ENGINE OVERHEATING", "YES", "COOLANT LEVEL LOW", "NO", "RADIATOR FAN WORKING", "YES"],  # Rule 8
    81: ["ENGINE PROBLEM", "YES", "ENGINE OVERHEATING", "NO", "ENGINE SHAKING", "YES", "SPARK PLUGS FOULED", "YES"],  # Rule 9
    91: ["ENGINE PROBLEM", "YES", "ENGINE OVERHEATING", "NO", "ENGINE SHAKING", "NO", "FUEL PRESSURE LOW", "YES"],  # Rule 10
    101: ["ENGINE PROBLEM", "YES", "ENGINE OVERHEATING", "NO", "ENGINE SHAKING", "NO", "FUEL PRESSURE LOW", "NO", "AIR FILTER DIRTY", "YES"],  # Rule 11
    111: ["CAR IS HAVING DIFFICULTY", "NO", "POOR ACCELERATION", "YES", "NOISE FROM ENGINE", "NO", "CAR JERK WHEN ACCELERATING", "YES"],  # Rule 12
    121: ["TRANSMISSION PROBLEM", "YES", "TRANSMISSION FLUID LOW", "YES"],  # Rule 13
    131: ["TRANSMISSION PROBLEM", "YES", "TRANSMISSION FLUID LOW", "NO", "CAR JERK WHEN SHIFTING GEARS", "YES"],  # Rule 14
    141: ["TRANSMISSION PROBLEM", "YES", "TRANSMISSION FLUID LOW", "NO", "CAR JERK WHEN SHIFTING GEARS", "NO", "TRANSMISSION NOISE WHEN ACCELERATING", "YES"],  # Rule 15
    151: ["TRANSMISSION PROBLEM", "YES", "TRANSMISSION NOISE WHEN ACCELERATING", "YES", "FLUID LEAKS UNDER THE CAR", "YES", "FLUID COLOR IS RED", "YES"],  # Rule 16
    161: ["CAR IS HAVING DIFFICULTY", "NO", "CANNOT SLOWDOWN WHEN BRAKING", "YES"],  # Rule 17
    171: ["BRAKE SYSTEM PROBLEM", "YES", "BRAKE PEDAL FEEL SPONGY", "YES", "BRAKE FLUID LEVEL LOW", "YES"],  # Rule 18
    181: ["BRAKE SYSTEM PROBLEM", "YES", "BRAKE PEDAL FEEL SPONGY", "YES", "BRAKE FLUID LEVEL LOW", "NO"],  # Rule 19
    191: ["BRAKE SYSTEM PROBLEM", "YES", "BRAKE PEDAL FEEL SPONGY", "NO", "BRAKE PEDAL HARD TO PRESS", "YES"],  # Rule 20
    201: ["BRAKE SYSTEM PROBLEM", "YES", "BRAKE PEDAL HARD TO PRESS", "NO", "CAR TAKES LONGER TO STOP", "YES"],  # Rule 21
    211: ["CAR IS HAVING DIFFICULTY", "NO", "STEERING FEEL LOOSE", "YES", "CAR PULLS TO ONE SIDE WHILE DRIVING", "YES"],  # Rule 22
    221: ["STEERING FEEL LOOSE", "YES", "CAR PULLS TO ONE SIDE WHILE DRIVING", "NO", "STEERING WHEEL VIBRATES", "YES", "VIBRATION WORSENS WHEN BRAKING", "YES"],  # Rule 23
    231: ["STEERING FEEL LOOSE", "YES", "CAR PULLS TO ONE SIDE WHILE DRIVING", "NO", "STEERING WHEEL VIBRATES", "YES", "VIBRATION WORSENS WHEN BRAKING", "NO"],  # Rule 24
    241: ["STEERING DIFFICULT TO TURN", "YES", "WHINING NOISE", "YES"],  # Rule 25
    251: ["STEERING DIFFICULT TO TURN", "YES", "WHINING NOISE", "NO"],  # Rule 26
    261: ["STEERING DIFFICULT TO TURN", "NO", "CLICKING NOISE", "YES"],  # Rule 27
    271: ["UNUSUAL NOISE FROM EXHAUST", "YES", "NOISE COMING FROM UNDER CAR", "YES"],  # Rule 28
    281: ["UNUSUAL NOISE FROM EXHAUST", "YES", "NOISE COMING FROM UNDER CAR", "NO", "EXHAUST SMELL INSIDE CAR", "YES"],  # Rule 29
    291: ["EXCESSIVE SMOKE FROM EXHAUST", "YES"]  # Rule 30
}



FORWARD_CLAUSE_VARIABLE_LIST = {
    1 : ["PROBLEM", "ELECTRICAL SYSTEM"],
    4 : ["PROBLEM", "STARTER"],
    7 : ["PROBLEM", "BATTERY"],
    10 : ["PROBLEM", "POWER STEERING PUMP"],
    13 : ["PROBLEM", "ENGINE"],
    16 : ["PROBLEM", "COOLANT LEAK"],
    19 : ["PROBLEM", "RADIATOR FAN"],
    22 : ["PROBLEM", "ENGINE MISFIRE"],
    25 : ["PROBLEM", "LOW FUEL PRESSURE"],
    28 : ["PROBLEM", "AIR INTAKE SYSTEM"],
    31 : ["PROBLEM", "TRANSMISSION"],
    34 : ["PROBLEM", "TRANSMISSION FLUID"],
    37 : ["PROBLEM", "TRANSMISSION SLIPPAGE"],
    40 : ["PROBLEM", "DAMAGED TRANSMISSION MOUNTS"],
    43 : ["PROBLEM", "TRANSMISSION FLUID LEAK"],
    46 : ["PROBLEM", "BRAKE SYSTEM"],
    49 : ["PROBLEM", "LOW BRAKE FLUID"],
    52 : ["PROBLEM", "AIR IN BRAKE LINES"],
    55 : ["PROBLEM", "VACUUM SYSTEM"],
    58 : ["PROBLEM", "WORN BRAKE PADS"],
    61 : ["PROBLEM", "STEERING/SUSPENSION"],
    64 : ["PROBLEM", "WARPED BRAKE ROTORS"],
    67 : ["PROBLEM", "UNBALANCED TIRES"],
    70 : ["PROBLEM", "LOW POWER STEERING FLUID"],
    73 : ["PROBLEM", "BINDING STEERING COMPONENTS"],
    76 : ["PROBLEM", "WORN CV JOINTS"],
    79 : ["PROBLEM", "LOOSE HEAT SHIELD"],
    82 : ["PROBLEM", "EXHAUST LEAK"],
    85 : ["PROBLEM", "COOLANT LEAK INTO ENGINE"],
    88 : ["PROBLEM", "ENGINE RUNNING RICH"],
    91 : ["PROBLEM", "ENGINE BURNING OIL"]
}



#PROBLEM LIST is a variable of datastructure list that will hold all the values of the disorder in the decison tree
PROBLEM_LIST = ["NO PROBLEM", "ELECTRICAL SYSTEM PROBLEM", "STARTER PROBLEM", "BATTERY PROBLEM", "POWER STEERING PUMP FAILURE", "ENGINE PROBLEM", 
                "COOLANT LEAK", "RADIATOR FAN MALFUNCTION", "ENGINE MISFIRE", "LOW FUEL PRESSURE", "AIR INTAKE SYSTEM PROBLEM", 
                "TRANSMISSION PROBLEM", "TRANSMISSION FLUID PROBLEM", "TRANSMISSION SLIPPAGE PROBLEM", "DAMAGED TRANSMISSION MOUNTS", "TRANSMISSION FLUID LEAK", 
                "BRAKE SYSTEM PROBLEM", "LOW BRAKE FLUID", "AIR IN BRAKE LINES", "VACUUM SYSTEM ISSUE", "WORN BRAKE PADS ISSUE", 
                "STEERING/SUSPENSION PROBLEM", "WARPED BRAKE ROTORS", "UNBALANCED TIRES", "LOW POWER STEERING FLUID", "BINDING STEERING COMPONENTS", 
                "WORN CV JOINTS", "LOOSE OR BROKEN HEAT SHIELD", "EXHAUST LEAK", "EXCESSIVE SMOKE FROM EXHAUST"
]


#backward and forward conclusion variables
backward_conclusions = None
forward_conclusions=None


#Intermediate nodes and derived variable list declaration
STACK_INTERMEDIATE_NODES=["PROBLEM"]
DERIVED_VARIABLE_LIST={}
DERIVED_FORWARD_VARIABLE_LIST ={}


#Main fucntion definition

def main():
        
    # Create and configure logger
    logging.basicConfig(filename="Project1-A05292110ITERATION_DETAILS.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    
    # Creating an object
    LOG = logging.getLogger()
    
    # Setting the threshold of logger to DEBUG
    LOG.setLevel(logging.DEBUG)
    
    LOG.info("PROGRAM START")
    LOG.info("DEFINING THE GOAL VARIABLE AS PROBLEM FOR BACKWARD CHAINING")
    LOG.info("CALLING BACKWARD CHAINING PROCESS FUNCTION")
    print("Kindly input YES or NO for each question" ,end='\n')
    goal_variable = "PROBLEM"
    start_time_bw = time.perf_counter()
    problem = BW.process(goal_variable)
    end_time_bw = time.perf_counter()

    LOG.info("THIS IS THE GOAL IDENTIFIED BY BACKWARD CHAINING ALGORITHM :%s "% problem)
    LOG.info("PASSING THE PROBLEM TO FORWARD CHAINING AND CALLING THE FORWARD CHAINING PROCESS FUNCTION")
    if problem not in [None, "NO PROBLEM"] and problem in PROBLEM_LIST:
        print("Your car has  : ", problem)
        start_time_fw = time.perf_counter()
        repair = FW.process(problem)
        end_time_fw = time.perf_counter()
        print("repair for" , problem, " is : ",repair)
        LOG.info("THIS IS THE GOAL IDENTIFIED BY FORWARD CHAINING ALGORITHM :%s "% repair)
        print(f"Time Elapsed for Forward chaining :  {end_time_fw - start_time_fw:0.2f} Secs")
    else:
        print("Your car doesn't have any problem so no repair required")
        LOG.info("No repair required")
    print(f"Time Elapsed for Backward chaining : {end_time_bw - start_time_bw:0.2f} Secs")
    memory = psutil.Process().memory_info().rss / (1024 * 1024)
    print("Memory consumed : ", memory, "MB")
if __name__ == "__main__":
    main()