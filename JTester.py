#Hoo boy have I forgotten python
#Runs program with all testcases, capture output, and match to solutions

import os
import subprocess
import linecache

testcases = ["testcase_1.txt"] #Global list of all test cases

##Prints specific difference between two lines in a file
def difference(line1, line2):
    print("Solution: " + line1)
    print("Output: " + line2)


##Compares the generated text files with solutions
##Returns amount of exact matches
def compare():
    cwd = os.getcwd()

    passes = 0
    case = 1
    for test in testcases:
        fsol = open(cwd + "/solution_" + test[9:-4] + ".txt")
        ftest = open(cwd + "/output_" + str(case) + ".txt")
        failed = False

        #While not reached either end of file
        linenum = 1
        while (line1 := fsol.readline()) and (line2 := ftest.readline()):
            if(line1 != line2):
                failed = True
                print("In case " + str(case) +", line "+ str(linenum) +" is different: ")
                difference(line1, line2)
            linenum += 1

        #Once finished a file       
        else:
            #line2 is shortcircuited out of the above while loop, so need
            #to run readline again to get them on the same line.
            line2 = ftest.readline()
            while(line1 != line2):
                failed = True
                print("In case " + str(case) + ", there are extra lines: ")
                difference(line1, line2)
                line1 = fsol.readline()
                line2 = ftest.readline()

            if not failed:
                passes += 1

        fsol.close()
        ftest.close()
        case += 1
    
    return passes


#Checks valgrind log file for leaks, saves file if there is
def memCheck(case, valgrindFile):
    cwd = os.getcwd()

    line = linecache.getline(valgrindFile, 12)
    s = ''.join(i for i in line if not i.isdigit()) #Remove process ID

    #Save file if leaks are present so it doesn't get overwritten
    if(s != "==== All heap blocks were freed -- no leaks are possible\n"):
        os.rename(cwd + "/" + valgrindFile, cwd + "/output_valgrind_" + str(case) + ".txt")
        print("Test case " + str(case) + "generated memory leaks!")

    
##Runs all test cases and produces output text files.
##Also handles runtime errors.
def runTests(doValgrind):

    case = 1
    for test in testcases:
        #Write output to file for later comparison and manual checking
        foutput = open("output_" + str(case) + ".txt", "w")

        
        #Run program, write stdout to file
        try:
            #User's choice to either check memory leaks or not for speed
            if(doValgrind == "y"):
                #Runs valgrind on each file and saves log to temp.txt
                proc = subprocess.run("valgrind --leak-check=full --log-file=temp.txt ./testsubject.out < " + test, capture_output=True, text = True, shell = True, timeout= 4) 
                memCheck(case, "temp.txt")
            else:
                proc = subprocess.run("./testsubject.out < " + test, capture_output=True, text = True, shell = True, timeout= 4)

            foutput.write(str(proc.stdout))
            foutput.close()
        
        #Program took more than 3 seconds to run
        except subprocess.TimeoutExpired as e:
            #If no output at all
            if(e.stdout == None):
                print("Test case " + str(case) + "- Program crashed or produced no output")
                foutput.write("! Crashed !\n")
                foutput.close()
            
            #Outputs, but still running a really long time
            else:
                print("Test case " + str(case) + "- Program is outputting for too long, likely an infinite loop")
                foutput.write("! Infinite loop !\n")
                foutput.close()

        #If error capture is not empty, display
        if(len(str(proc.stderr)) > 0):
            print("Test case " + str(case) + "- Program had error messages:")
            print(str(proc.stderr))

        print("Test " + str(case) + " finished")
        case += 1 #Move on to next case

    #Finished with all cases
    if(doValgrind == "y"): 
        os.remove(os.getcwd() + "/temp.txt") 
        linecache.clearcache() #Clears cache from all the valgrinds
    print("Finished testing all cases")


##Ensures test cases, solutions, and executable all exist before beginning
def checkSetup():
    cwd = os.getcwd()

    #Ensure all test cases and solutions exist for all specified at top of file
    case = 1
    for test in testcases:
        num = test[9:-4] #Gets number in textcase name
        if not os.path.exists(cwd + "/testcase_" + str(num) + ".txt"):
            print("Test case " + str(case) + ", 'testcase_" + str(num) + ".txt' is missing!")
            exit(0)
        if not os.path.exists(cwd + "/solution_" + str(num) + ".txt"):
            print("Solution file " + str(case) + ", 'solution_" + str(num) + ".txt' is missing!")
            exit(0)

        case += 1

    #Check if executable exists
    if not os.path.exists(cwd + "/testsubject.out"):
        print("Executable file 'testsubject.out' not found")
        exit(0)


def main():
    #Greeting
    print("------------------------------------------------")
    print("~~~\tJohn-test-o-matic-inator, v1.1\t~~~\n")
    print("'I don't wanna type those test cases")
    print("so I'll script it.' -A Fool (me)\n")
    print("Compares generated test cases against your compiled solution")
    print("Name your test cases as 'testcase_x.txt' and 'solution_x.txt'")
    print("Make sure your program is compiled as 'testsubject.out'!")
    print("(gcc -o testsubject.out programname.c)")
    print("------------------------------------------------")

    #Define number of cases in global list
    num = input("How many cases: ")
    for i in range(1, int(num)):
        testcases.insert(i, "testcase_" + str(i+1) + ".txt")

    doValgrind = input("Run valgrind? Will significantly slow runtime. (y/n): ") 

    print("Checking if everything is in order...")
    checkSetup()
    print("All good! Beginning tests...")
    runTests(doValgrind)
    print("All tests done, comparing with solutions...")

    if(compare() == len(testcases)): #As many successes as testcases
        print("YIPPPEEEEE")
    else:
        print(":(")



if __name__ == "__main__":
    main()