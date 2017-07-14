import imaplib
# Original Script by Cadellin.
# Accessing email account
M = imaplib.IMAP4_SSL('imap.gmail.com')
try:
    M.login('youremailinhere', 'yourpasswordinhere')
    print("logged in")
except imaplib.IMAP4.error:  # On failure
    print("Login failed")
M.select("INBOX")

# All sales emails in inbox- add value in GBP to list, put original emails into a folder, marked read
# If you want to present the data in a different currency, tweak the values below. GBP is default.
listy = []
typ, dataraw = M.search(None, '(FROM "congratulations@redbubble.com")')
for num in dataraw[0].split():
    result = M.store(num, '+X-GM-LABELS', 'yourdestinationfolder')
    result = M.store(num, '+FLAGS', '\\Deleted')
    typ, data = M.fetch(num, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')
    data = [x[-1] for x in data]
    data = str(data)
    "".join(data)
    if "=28=C2=A3" in data:             #Pounds
        data = data.split('=28=C2=A3')
        data = data[-1]
        data = data.split('=')
        data = data[0]
    elif "=28=E2=82=AC" in data:        #Euros
        data = data.split('=28=E2=82=AC')
        data = data[-1]
        data = data.split('=')
        data = data[0]
        data = (float(data) * 0.88)
    else:                               #US Dollars
        data = data.split('(US$')
        data = data[-1]
        data = data.split(')')
        data = data[0]
        data = (float(data) * 0.77)
    data = round(float(data), 2)
    listy.append(data)

#get dates of emails, also marks as read
listdates = []
for num in dataraw[0].split():
    typ, dates = M.fetch(num, '(BODY[HEADER.FIELDS (RECEIVED DATE)])')
    dates = [x[-1] for x in dates]
    dates = str(dates)
    "".join(dates)
    dates = dates.split(' ')
    dates = dates[8] + ' ' + dates[9] + ' ' + dates[10]
    dates = dates.replace('\\r\\n', '')
    listdates.append(dates)

#add days with more than one payment together. Bubble sort, kinda.
rand=len(listy)-1
goku = 0
for i in range(rand):
    if listdates[i] == listdates[i + 1]:
        goku += 1
for i in range(goku):
    for i in range(rand):
        if listdates[i] == listdates[i+1]:
            listy[i] = str(round(float(listy[i]) + float(listy[i+1]), 2))
            listy[i+1] = str(0)
for i in reversed(range(len(listy))):
    if listy[i] == "0" or listy[i] == "0.0":
        del listy[i]
        del listdates[i]

#print results
for i in range(len(listdates)):
    print(str(listdates[i]) + ": £" + str(listy[i]))

#cleanup
M.expunge()
M.close()
M.logout()