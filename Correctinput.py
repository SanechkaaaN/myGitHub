def correct_input(commands:list[str])->bool:
    if len(commands)<2:
        return False

    if commands[1]!="init" or commands[1]!="commit" or commands[1]!= "checkout":
        return False

    if commands[1]=="init" and len(commands)!=2:
        return False

    if (commands[1]=="commit" or commands[1]=="checkout") and len(commands)<3:
        return False

    if commands[1]=="commit" and commands[2].strip()=="":
        return False

    return True