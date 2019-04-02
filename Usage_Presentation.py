
# coding: utf-8

# In[1]:


from textpatternrecognition.pattern import PatternParser


# Looking for *multiline* patterns that may overlap in a left to right and top down perspective

# for example pattern:
#  | |
#  ###O
#  | |
# should be found 3 times in
#
#    | |
#    ###O
#    | |           | |
#                  ###O
#                  | |              | |
#                                   ###O
#                                   | |
#
# ## Content

# 1. Finding Only One Pattern
#   1. Single-Line Pattern
#   2. Multi-Line Pattern
# 2. Finding Multiple Patterns (with mixed line number and RegEx's)
# 3. Some Performance Check – a little random

# # Finding Only One Pattern

# ## Single Line Pattern

# In[2]:


pattern = 'ab'


# In[3]:


text_lines = [
    'ab der zeile 0',
    'wird über eine Datei',
    'zeile für zeile',
    'iteriert und gesucht',
    'wie häufig das wort ab ab zeile 0 vorkommt', # works with utf-8, if using other encodings should handle it on file read level
]


# In[4]:


pattern_parser = PatternParser(pattern)


# In[5]:


found = 0
for n, line in enumerate(text_lines):
    found_in_line = pattern_parser.parse_text(line)
    print(f'{n}: {found_in_line}\t({line})')
    found += found_in_line
print('Found:', found)


# #### Let's do a regex!

# In[6]:


regex_pattern = 'a.'


# In[7]:


pattern_parser = PatternParser(regex_pattern, use_regex=True)


# In[8]:


found = 0
for n, line in enumerate(text_lines):
    found_in_line = pattern_parser.parse_text(line)
    print(f'{n}: {found_in_line}\t({line})')
    found += found_in_line
print('Found:', found)


# ## Multi Line Pattern

# ### Bug-1.txt

# In[9]:


bug_1_pattern = '''| |
###O
| |'''
print(bug_1_pattern)


# ### landscape1.txt

# In[10]:


landscape_1_text = '''                                       
    | |                                
    ###O                               
    | |           | |                  
                  ###O                 
                  | |              | | 
                                   ###O
                                   | | 
'''
print(landscape_1_text)


# In[11]:


pattern_parser = PatternParser(bug_1_pattern)
lines = landscape_1_text.splitlines()
found = 0
for n, line in enumerate(lines):
    found_in_line = pattern_parser.parse_text(line)
    print(f'{n}: {found_in_line}\t({line})')
    found += found_in_line
print('Found:', found)


# # Finding multiple Patterns

# In[12]:


additional_pattern_regex = ':-.'


# In[13]:


pattern_parser_1 = PatternParser(bug_1_pattern, use_regex=False)
pattern_parser_2 = PatternParser(additional_pattern_regex, use_regex=True)


# In[14]:


landscape_1_text = '''                                       
    | |                        :-)                 
    ###O                               
    | |           | |                  
                  ###O                 
                  | |              | | 
                                   ###O
    :-(                            | | 
'''
print(landscape_1_text)


# In[15]:


bugs = 0
smileys = 0
for line in landscape_1_text.splitlines():
    bugs += pattern_parser_1.parse_text(line)
    smileys += pattern_parser_2.parse_text(line)
print(f'{bugs} bugs & {smileys} smileys found')


# # Performance

# Not really a good performance test – I am just curious.
# 
# By the way – this is run on a really slow laptop.

# In[16]:


from random import choices
from string import ascii_lowercase


# In[17]:


def search_for_pattern_in_long_text(pattern='x\ny\nz\n',lines=10**4, line_length=150, use_regex=True):
    pattern_parser = PatternParser(pattern, use_regex=use_regex)
    found = 0
    for index in range(lines):
        line = ''.join(choices(ascii_lowercase, k=line_length))
        found += pattern_parser.parse_text(line)
    return found


# In[18]:


# Once for fun
search_for_pattern_in_long_text()


# In[19]:

# Check for jupyter / ipython compatibility
#get_ipython().run_cell_magic('timeit', '', 'search_for_pattern_in_long_text(use_regex=True)')


# In[20]:

# Check for jupyter / ipython compatibility
#get_ipython().run_cell_magic('timeit', '', 'search_for_pattern_in_long_text(use_regex=False)')

