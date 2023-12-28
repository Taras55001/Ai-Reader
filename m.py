from PyPDF2 import PdfReader 
  
# creating a pdf reader object 
reader = PdfReader('Siromanets.pdf') 
  

print(len(reader.pages)) 
  

page = reader.pages[0] 
  

text = page.extract_text() 
print(text) 