import wikipedia

wikipedia.set_user_agent('uz')
print(wikipedia.search('urgench'))
print(wikipedia.summary('urgench'))