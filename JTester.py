#Hoo boy have I forgotten python
#Runs program with all testcases, capture output, and match to solutions

import os
import subprocess

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
        ftest = open(cwd + "/output_testcase_" + str(case) + ".txt")
        failed = False

        #While not reached either end of file
        while (line1 := fsol.readline()) and (line2 := ftest.readline()):
            if(line1 != line2):
                failed = True
                print("In case " + str(case) +", this line is different: ")
                difference(line1, line2)

        #Once finished a file       
        else:
            #line2 is shortcircuited out of the above while loop, so need
            #to run readline again to get them on the same line.
            while(line1 != (line2 := ftest.readline())):
                failed = True
                print("In case " + str(case) + ", there are extra lines: ")
                difference(line1, line2)
                line1 = fsol.readline()

            if not failed:
                passes += 1

        fsol.close()
        ftest.close()
        case += 1
    
    return passes
    
##Runs all test cases and produces output text files.
##Also handles runtime errors.
def runTests():

    case = 1
    for test in testcases:
        #Write output to file for later comparison and manual checking
        foutput = open("output_testcase_" + str(case) + ".txt", "w")

        #Run program, write stdout to file
        try:
            ##Maybe change to 'valgrind --log-file=temp.txt ./testsubject.out < test' to check mem leaks?
            proc = subprocess.run("./testsubject.out < " + test, capture_output=True, text = True, shell = True, timeout= 3) 
            foutput.write(str(proc.stdout))
            foutput.close()
        
        #Program took more than 3 seconds to run
        except subprocess.TimeoutExpired as e:
            #If no output at all
            if(e.stdout == None):
                print("Test case " + str(case) + "- Program crashed or produced no output")
                foutput.write("! Crashed !\n")
            
            #Outputs, but still running a really long time
            else:
                print("Test case " + str(case) + "- Program is outputting for too long, likely an infinite loop")
                foutput.write("! Infinite loop !\n")

        #If error capture is not empty, display
        if(len(str(proc.stderr)) > 0):
            print("Test case " + str(case) + "- Program had error messages:")
            print(str(proc.stderr))

        case += 1 #Move on to next case

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
    print("~~~\tJohn-test-o-matic-inator, v1\t~~~\n")
    print("'I don't wanna type those test cases")
    print("so I'll script it.' -A Fool (me)\n")
    print("For use with JTCGen.c")
    print("Compares generated test cases against your compiled solution")
    print("Make sure your program is compiled as 'testsubject.out'!")
    print("(gcc -o testsubject.out programname.c)")
    print("------------------------------------------------")

    #Define number of cases in global list
    num = input("How many cases: ")
    for i in range(1, int(num)):
        testcases.insert(i, "testcase_" + str(i+1) + ".txt")

    print("Checking if everything is in order...")
    checkSetup()
    print("All good! Beginning tests...")
    runTests()
    print("All tests done, comparing with solutions...")

    if(compare() == len(testcases)): #As many successes as testcases
        print("YIPPPEEEEE")
    else:
        print(":(")



if __name__ == "__main__":
    main()