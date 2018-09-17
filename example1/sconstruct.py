import os
import sys
import SCons.Script
from SCons.Environment import Environment

# Setup the construction env
tools = ['gcc']
env = Environment(tools=tools)
env.EnsureSConsVersion(3, 0, 0)

#env.Replace(ENV=os.environ)
env.Replace(ENV={'PATH': os.environ['PATH']})

# File list of files
env.Replace(ExampleList1=[env.File('../src1 with spaces/src1.c')])
env.Append(ExampleList1=['../src1 with spaces/src2.c'])
env.Append(ExampleList1=['../src1 with spaces/src3.c'])

# Lets create a 2nd list of files
env.Replace(ExampleList2=[
    '../src2 with spaces/src4.c',
    '../src2 with spaces/src5.c',
    '../src2 with spaces/src6.c'])


# Lets Join both lists of files to simulate nested variable substitution
env.Replace(SRCS='$ExampleList1 $ExampleList2')


# Lets try printing the list of items using split
print("\nSplit Items")
splititems = env.Split('$SRCS')
for item in splititems:
    print(str(item))

# Lets try printing the list of items using env.subst
print("\nenv.subst Items")
substitems = env.subst('$SRCS')
for item in splititems:
    print(str(item))

# Nearly works but the end result is wrapped in a string
print("\nenv.subst Items with lambda")
substitems2 = env.subst('$SRCS', conv=lambda x: x)
print(substitems2)

# Lets try printing the list of items using env.subst
print("\nenv.subst_list Items")
substitems3 = env.subst_list('$SRCS')[0]
for item in substitems3:
    print(str(item))

# Doesnt recurse expand
print("\n env.Dictionary test")
dict1 = env.Dictionary('SRCS')
print(dict1)
print('\n')

# Could only get this to work with env.subst_list('$SRCS')[0]
# I feel im missing something obvious
def build(target, source, env):
    print("\nCommand sources")
    for item in source:
        print(str(item))
    return None
#Command('foo.out', '$SRCS', build)
#env.Command('foo.out', '$SRCS', build)
