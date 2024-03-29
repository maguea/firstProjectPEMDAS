#Pemdas
#Terminal calculator that solves basic equations in PEMDAS order
#Instructions: Program will ignore white space, and correct minor misinputs.
#Program Syntax:
#   '(' to begin a parnethesis, ')' to close parenthesis 
#   '^' for power of
#   '*' for multiplication, and '/' for division
#   '+' for addition, and '-' for subtraction
#   '.' to add a decimal point
#   To take a root, use the power rule (e.g. square root of 4 is written as "4^(1/2)")
#No support for Euler's number (e) or logs
#Hit enter after typing equation (you can include or omit '=' sign)

#-----------code below-----------#

#Start loop to keep program open
def start():
    initialEq = input("Enter equation (Type \"c\" to close program): ")
    if initialEq != "c" and initialEq != "C":
        breakUp(initialEq)
    else:
        print("Thank you, goodbye.")

#Directs input str into a total    
def breakUp(initialEq):
    attach = 0
    listed = list()
    removes = list()
    listed.extend(initialEq)
    oParCnt = listed.count('(')
    cParCnt = listed.count(')')
    for x in listed:
        if (isOp(x) == False) and (x != '(') and (x != ')') and (x!='.'):
            try:
                float(x)
            except:
                print("\"" + str(x) + "\" has been automatically removed.")
                removes.append(x)
    for x in removes:
        listed.remove(x)
    if not listed:
        print("No equation left.")
    else:
        if oParCnt and cParCnt:
            listed, oParCnt, cParCnt, attach = crabLegs(listed, attach)
        listed, finalEq = repair(listed, oParCnt, cParCnt, attach)
        nums, sigs = delimit(listed)
        total = eqCheck(nums, sigs)
        print(finalEq + ' = ' + str(total))
    start()

#Fixes specific error where equation has ) * (
def crabLegs(listed, attach):
    oPar = listed.index('(')
    cPar = listed.index(')')
    if cPar < oPar:
        listed.append(')')
        attach += 1
    oParCnt = listed.count('(')
    cParCnt = listed.count(')')
    return(listed, oParCnt, cParCnt, attach)           

#Checks equations and fixes possible errors
def repair(listed, oParCnt, cParCnt, attach):
    if isOp(listed[-1]) or listed[-1] == '(':
        print("An extra operator \"" + listed[-1] + "\" has been found at the end of the equation. Automatically removed.")
        listed.pop()
    if (oParCnt != 0) or (cParCnt != 0):
        if oParCnt > cParCnt:
            while oParCnt != cParCnt:
                listed.append(')')
                cParCnt += 1
                attach += 1
        if oParCnt < cParCnt:
            while oParCnt != cParCnt:
                listed.insert(0, '(')
                oParCnt += 1
                attach += 1
        print("Parentheses have not been properly closed. Automatically added "+ str(attach) +" parentheses.")
        finalEq = ''.join(listed)
        listed = innerDel(listed, oParCnt)
    else:
        finalEq = ''.join(listed)
    return(listed, finalEq)

#Boolean check if x is an operator
def isOp(x):
    if (x == '+') or (x == '-') or (x == '*') or (x == '/') or (x == '^'):
        return True
    else:
        return False

#Isolates parenthesis equations       
def innerDel(listed, oParCnt):
    x = 0
    innerPar = list()
    while oParCnt > 0:
        if listed[x] == '(':
            oParCnt -= 1
        x+=1
    while listed[x] != ')':
        innerPar.append(listed[x])
        listed.pop(x)
    nums, sigs = delimit(innerPar)
    replace = eqCheck(nums, sigs)
    listed[x-1] = str(replace)
    listed.pop(x)
    newOPar = listed.count('(')
    if newOPar > 0:
        listed = innerDel(listed, newOPar)
    return(listed)

#Create 2 lists for operators and numbers
def delimit(listed):
    sigs = list()
    nums = list()
    tempHold = ''
    x = 0
    tempHold+=listed[x]
    x+=1
    while x < len(listed):
        if isOp(listed[x]):
            finalFloat = floatCheck(tempHold)
            if finalFloat != 'skip':
                nums.append(finalFloat)
            tempHold = ''
            if isOp(listed[x+1]) and (listed[x+1] != '-'):
                print("Extra operator: \"" + listed[x+1] + "\" has been found, automatically removed.")
                listed.pop(x+1)
            sigs.append(listed[x])
            x+=1        
        tempHold += listed[x]
        x+=1
    nums.append(floatCheck(tempHold))
    return(nums, sigs)

#final check to limit number input error
def floatCheck(input):
    try:
        float(input)
        return(float(input))
    except:
        numCheck = list()
        numCheck.extend(input)
        decPoints = numCheck.count('.')
        while decPoints > 1:
            numCheck.remove('.')
            decPoints -= 1
        try:
            return(float(''.join(str(x) for x in numCheck)))
        except:
            return('skip')

#Checks operator list for mixed order
def eqCheck(nums, sigs):
    newNum = list()
    exp = sigs.count('^')
    muDi = sigs.count('*') + sigs.count('/')
    plMi = sigs.count('+') + sigs.count('-')
    total = nums[0]
    while (len(sigs) - plMi) > 0:
        x = 0
        while exp > 0:
            x = sigs.index('^')
            exp -= 1
            newNum.extend((nums[x], nums[x+1]))
            total = expo(newNum, sigs[x-1])
            nums.pop(x+1)
            nums[x] = total
            sigs.pop(x)
            newNum.clear()
        x = 0
        newNum.clear()
        while muDi > 0:
            if sigs.count('*') > 0:
                x = sigs.index('*')
            if sigs.count('/') > 0:
                x = sigs.index('/')
            muDi-=1
            newNum.extend((nums[x], nums[x+1]))
            total = mulDi(newNum, sigs[x])
            if total == 'Cannot divide by 0, try again.':
                return('Cannot divide by 0, try again.')
            nums.pop(x+1)
            nums[x] = total
            sigs.pop(x)
            newNum.clear()     
    if plMi > 0:
        total = adSub(nums, sigs)
    return(total)

#Calculate addition and subtraction in order
def adSub(nums, sigs):
    x = 1
    z = 0
    total = nums[0]
    sigs.append(' = ')
    while x < len(nums):
        input = nums[x]
        if sigs[z] == '-':
            total -= input
            z+=1
        elif sigs[z] == '+':
            total += input
            z+=1
        else:
            break
        x+=1
    return(total)

#Calculate multiplication and division in order
def mulDi(nums, sigs):
    if sigs[0] == '/':
        if nums[1] != 0:
            total = nums[0] / nums[1]
            return(total)
        else:
            print('Cannot divide by 0, try again.')
    if sigs[0] == '*':
        total = nums[0] * nums[1]
        return(total)

#Calculate exponents in order        
def expo(nums, sigs):
    x = len(sigs)
    total = nums[x]
    while x > 0:
        total = nums[x-1] ** total
        x-=1
    return(total)

#Initializes program loop
start()
