import sys

# global variables
attr_list=["Customers.Name","Customers.Age", "Orders.CustomerName","Orders.Product","Orders.Price","*"]
tables=["Customers","Orders"]
operators=["<=",">=","<>","<",">","="]

#returns all occurrences of operator
def find_operator_indexes (word, sentence):
    index = 0;
    lst=[]
    while index < len(sentence):
        index = sentence.find(word, index)
        if index == -1:
            break
        lst.append(index)
        index += len(word)
    return lst

# split string to 3 parts: 1) between SELECT-FROM, 2) between FROM-WHERE 3) between WHERE-END
def split_str(str):
    queryParts=str.split("FROM")
    queryParts[0]=queryParts[0].replace("SELECT",'')
    selectText=queryParts[0].strip()
    selectText=" ".join(selectText.split()) #remove multiply spaces
    queryParts1=queryParts[1].split("WHERE")
    fromText=queryParts1[0].strip()
    fromText=" ".join(fromText.split())  #remove multiply spaces
    whereText=queryParts1[1].strip()
    whereText=" ".join(whereText.split())  #remove multiply spaces
    lst=[selectText,fromText,whereText]
    return lst

#recursive func - check if the attributes are valid    
def is_attribute_list(str, fromText):
    if("," not in str):
        str=str.strip()
        return is_attribute(str,fromText)
    else:
        if ("*" in str and "," in str): # "*" must be the only attribute
            return False
        
        str=str.strip()
        #distinct must be used on first attribute
        if(("DISTINCT" in str) and ("DISTINCT" not in str[0:8])): 
            return False
        
        newStr=str.split(",",1) 
        newStr[0]=newStr[0].strip()
        res1=is_attribute(newStr[0], fromText)
        res2=is_attribute_list(newStr[1], fromText)
        if((res1 and res2)!=True):
            return False
        else:
            return True

#check if single attribute is valid
def is_attribute(str, fromText):
    res=False
    tempStr=str.split(' ',1)
    if((tempStr[0] == "DISTINCT") or (tempStr[0] == "DISTINCT*")):
        tempStr[0]=tempStr[0].replace("DISTINCT","")
        str=' '.join(tempStr)
        str=str.strip()
        
    if (str in attr_list):
        res=is_table_in_str(str, fromText)
        
    return res

def is_table_in_str(str, fromText):
    lst=fromText.split(",")
    for table in lst:
        table=table.strip()
        if(table in str):
            return True
    return False

#recursive func - check if the table lists are valid
def is_table_list(str): 
    if("," not in str):
        return is_table(str)
    else:
        newStr=str.split(",",1)
        newStr[0]=newStr[0].strip()
        newStr[1]=newStr[1].strip()
        res1=is_table(newStr[0])
        res2=is_table_list(newStr[1])
        if(res1 and res2!=True):
            return False
    return True
     
#check if single table name is valid      
def is_table(str):
    if(str in tables):
        return True
    return False

#recursive func - check if the condition is valid by spliting the string by operators
def is_condition(str, fromText):
    resLeft=resRight=False
    resCond=False
    if(is_simple_condition(str, fromText)):
        return True

    else:
        #build list of operator indexes
        lst_of_AND=find_operator_indexes("AND", str) 
        lst_of_OR=find_operator_indexes("OR", str)
        listOfOperatos=lst_of_AND+lst_of_OR
        listOfOperatos.sort()
        
        #splitting the string by operators 
        for oper_index in listOfOperatos:
            if(str[oper_index]=='A'):
                wordLen=3
            else:
                wordLen=2
        
            leftStr=str[0:oper_index-1]
            rightStr=str[oper_index+wordLen+1:]
            
            resLeft=is_condition(leftStr, fromText)
            resRight=is_condition(rightStr, fromText)
            
            if(resLeft and resRight):
                return True
            
        #delete not-needed brackets
        if(str[0]=='(' and str[-1]==')'):
            str=str[1:-1]  
            resCond=is_condition(str, fromText)            

        return resCond

        
#check if simple condition is valid      
def is_simple_condition(str, fromText):    
    operVal=""
    
    
    #delete not-needed brackets
    while(str[0]=='(' and str[-1]==')'):
         str=str[1:-1]
    
    for item in operators:
        if (item in str):
            operVal=item
            break
    if(operVal==""):
        return False
    else:
        newStr=str.split(operVal,1)
        newStr[0]=newStr[0].strip()
        newStr[1]=newStr[1].strip()
        
        res1=is_constant(newStr[0], fromText)
        res2=is_constant(newStr[1], fromText)
        
        #check if constant types is equal      
        if(res1[0] and res2[0]):
            if(res1[1]=="Attribute"):
                if(is_table_in_str(newStr[0], fromText)):
                    if((res2[1]=="Attribute") and (is_table_in_str(newStr[1], fromText))):
                         return True
                    elif (("Name" in newStr[0]) or ("Product" in newStr[0])):
                        if(res2[1]=="String"):
                            return True
                    elif(("Age" in newStr[0]) or ("Price" in newStr[0])):
                        if(res2[1]=="Digit"):
                            return True
            elif(res1[1]==res2[1]):
                return True
                        
    return False

def is_constant(str, fromText):
    #checking what is the type of each constant
    if (str): # if str is not empty
        if(str.isdigit()):
           return [True, "Digit"]
        elif(is_attribute(str,fromText)):
            return [True, "Attribute"]
        elif((str[0]=='\"' and str[-1]=='\"' ) or (str[0]=='\'' and str[-1]=='\'' )):
            return [True, "String"]
    
    return [False,""]


def main():
    isSelectOk = isFromOk = isWhereOk = False
    str=input("Enter your query: ")
    str=str.strip()
    
    if(str[-1]!=";"):
        sys.exit("invalid") #query must end with ;
    
    str=str[0:-1] # remove ;  
    lst=split_str(str)  #split the query to 3 parts - select, from, where
    isSelectOk=is_attribute_list(lst[0],lst[1])
    if(isSelectOk):
        isFromOk=is_table_list(lst[1])
    else:
        sys.exit("invalid\nParsing <attribute_list> failed")
    
    if(isFromOk):
        isWhereOk=is_condition(lst[2], lst[1])
    else:
        sys.exit("invalid\nParsing <table_list> failed")
    
    if(isWhereOk):
        print("valid")
    else:
        sys.exit("invalid\nParsing <condition> failed")
        
if __name__ == "__main__":
    main()