# Extract all the important info from the grammar and string files
def read_grammar_file(filename):
    with open(filename, "r") as file:
        lines = file.read().strip().split(";")  # Split rules using semicolon

    Grammer = [line.strip().split(" -> ") for line in lines if "->" in line]  # Parse rules
    NumOfNotations = len(Grammer)  # Count the number of grammar rules

    return NumOfNotations, Grammer

def read_string_file(filename):
    with open(filename, "r") as file:
        String = file.readline().strip()  # Read the single-line string
        
    return String

# Check the grammar rules to make sure they follow the correct format and all variables are defined
def check_grammer(Grammer):
    Variables = {}
    for Notation in Grammer:
        if len(Notation[0]) != 1 or not (Notation[0].isupper()):
            return False
        if Notation[0] not in Variables or Variables[Notation[0]] == "undefined":
            Variables[Notation[0]] = "defined"
        if len(Notation[1]) > 2 or len(Notation[1]) == 0:
            return False
        if len(Notation[1]) == 1 and not (Notation[1][0].islower()):
            return False
        if len(Notation[1]) == 2:
            if not (Notation)[1][0].isupper() or not (Notation)[1][1].isupper():
                return False
            for i in range(2):
                if Notation[1][i] not in Variables:
                    Variables[Notation[1][i]] = "Undefined"
    for Value in Variables.values():
        if Value == "undefined":
            return False
    return True

# CYK algorithm implementation
def cyk(String, Computed=None, Grammer=None):
    if Computed is None:
        Computed = {}  # Initialize if not provided
    if Grammer is None:
        raise ValueError("Grammar must be provided")  # Ensure grammar is passed

    if String in Computed:
        return Computed
    else:
        if len(String) == 1:
            Computed[String] = ""
            for Notation in Grammer:
                if Notation[1] == String:
                    Computed[String] += Notation[0]
            Computed[String] = str(sorted(Computed[String])).replace(
                "'", "").replace(" ", "")
            return Computed
        else:
            Computed[String] = ""
            for i in range(1, len(String)):
                Splitted1 = String[:i]
                Splitted2 = String[i:]
                Computed1 = cyk(Splitted1, Computed, Grammer)[Splitted1]
                Computed2 = cyk(Splitted2, Computed, Grammer)[Splitted2]
                if Computed1 != "" and Computed2 != "":
                    for Var1 in Computed1:
                        for Var2 in Computed2:
                            for Notation in Grammer:
                                if Var1 + Var2 in Notation[1] and Notation[0] not in Computed[String]:
                                    Computed[String] += Notation[0]
            Computed[String] = str(sorted(Computed[String])).replace(
                "'", "").replace(" ", "")
            return Computed

# Prints 0 if the string can be parsed by the grammar, otherwise prints 1, along with the parse details.
def print_cyk(String, Grammer):
    result = cyk(String, {}, Grammer)
    if result[String] != "[]" and "S" in result[String]:
        print(0)
        for i in range(1, len(String)+1):
            for j in range(len(String) - i):
                if String[j:j+i] in result:
                    print(String[j:j+i]+" : " +
                          result[String[j:j+i]]+" , ", end="")
                else:
                    print(String[j:j+i]+" : "+"[]"+" , ", end="")
            print(String[-i:], " : "+result[String[-i:]])
    else:
        print(1)

# Get user input for their file paths
grammartext = input("Please enter the path to your grammar file: ")
stringtext = input("Please enter the path to your string file: ")

# Collect all the important info
NumOfNotations, Grammer = read_grammar_file(grammartext)
String = read_string_file(stringtext)

# Check if string in grammar
if check_grammer(Grammer):
    print_cyk(String, Grammer)
else:
    print("Invalid Grammar")