import concurrent.futures
import multiprocessing as mp
import re
import time
import os

import pandas as pd
from validate_email import validate_email

#from validate_email_address import validate_email

start = time.perf_counter()

def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      return True
    else:
      return False


emails_main = "C:/Users/João/Documents/base_joao_100.csv"
cpu_n = int(mp.cpu_count())
print(cpu_n)
number_lines = int(sum(1 for row in (open(emails_main))))
rowsize = int(round(number_lines / cpu_n))
print(rowsize)
l = int(input("What's the number of the row that the emails are at?"))
names_list = []
for i in range(1,number_lines, rowsize):
    df = pd.read_csv(emails_main,
          usecols=[l],
          header = None,
          nrows = rowsize,
          skiprows = i)

    df.set_axis(["email"],axis=1, inplace=True) # type: ignore
    df.head()
    out_csv= 'email' + str(i) + '.csv'
    names_list.append(out_csv)
    df.to_csv(out_csv,
          index=False,
          header=True,
          mode='a',#append data to csv file
          chunksize=rowsize)#size of data to append for each loop
    
def main(prompt):
        valid_email = []
        invalid_email = []
        line_count= 0 
        start_ = time.perf_counter()
        email_num = pd.read_csv(prompt, usecols=[l])
        for x, emoil in email_num.iterrows():
                if line_count == 0:  
                    line_count += 1   
                else:
                    line_count += 1
                    email = emoil['email']
                    isexist=validate_email(email, smtp_timeout=1, dns_timeout=1)
                    print(f"""------------------------------------------------------------------------------------
email: {email}
valido = {isexist}
place = {line_count}/{rowsize}""")
                    if isexist == True:
                        valid_email.append(email)
                    elif isexist == None:
                        invalid_email.append(email)
                    elif isexist == False:
                        invalid_email.append(email)

                    elif isexist == 'True':
                        valid_email.append(email)
                    elif isexist == 'None':
                        invalid_email.append(email)
                    elif isexist == 'False':
                        invalid_email.append(email)

                    else:
                        invalid_email.append(email)
        finish_ = time.perf_counter()
        for o in range(10):
            print("--------------------------------------------------------------------------------------------------------------------")
        print(f"finish time for file:{prompt} time: {finish_-start_}")
        if(os.path.exists(prompt) and os.path.isfile(prompt)):
            os.remove(prompt)
            print("file deleted")
        else:
            print("file not found")
        cleber = [valid_email, invalid_email]
        return cleber


with concurrent.futures.ThreadPoolExecutor() as executor:
    main_valid_email = []
    main_invalid_email = []
    results = executor.map(main, names_list)
    
    for result in results:
        for result in results:
            for _ in result[0]:
                main_valid_email.append(_)
            for __ in result[1]:
                main_invalid_email.append(__)
    print(len(main_valid_email))
    print("------------")
    print(len(main_invalid_email));
    for o in range(10):
            print("*--------------------------------------------------------------------------------------------------------------------*")
    print(main_valid_email)
    print(main_invalid_email)
        
finish = time.perf_counter()
finish_timer = round(round(finish-start, 2) / 60)
print(f'Finished in {round(finish-start, 2)}seconds, {finish_timer} minutes')