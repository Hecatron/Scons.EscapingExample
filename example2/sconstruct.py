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

# Compiler commands
# This is just because I happen to have the arm version of gcc setup on windows at the time
env.Replace(CROSS_COMPILE='arm-none-eabi-')

env.Replace(AS='${CROSS_COMPILE}as')
env.Replace(CC='${CROSS_COMPILE}gcc')
env.Replace(CPP='${CROSS_COMPILE}gcc')
env.Replace(CXX='${CROSS_COMPILE}g++')
env.Replace(LD='${CROSS_COMPILE}ld')
env.Replace(OBJCOPY='${CROSS_COMPILE}objcopy')
env.Replace(SIZE='${CROSS_COMPILE}size')
env.Replace(STRIP='${CROSS_COMPILE}strip')
env.Replace(AR='${CROSS_COMPILE}ar')


# Lets try adding some cpppath's
env.AppendUnique(CPPPATH=[env.GetLaunchDir()])
env.AppendUnique(CPPPATH=['testdir'])
env.AppendUnique(CPPPATH=['../src1 with spaces'])

# The first 3 examples below work fine with CPPPATH

def example1():
    # At this stage we're testing the wrappering of CPPPATH with quotes for include directories
    # This works fine / is properly quoted and escaped
    env.Object('src1.o', '../src1 with spaces/src1.c')

def example2():
    # Use Command with action
    # This works fine / is properly quoted and escaped
    act = SCons.Action.Action('${CPP} ${CFLAGS} ${CCFLAGS} ${_CCCOMCOM} -c -o ${TARGET} ${SOURCES}')
    env.Command('src1.o', '../src1 with spaces/src1.c', act)

def example3():
    # Use Command with string
    # This works fine / is properly quoted and escaped
    env.Command('src1.o', '../src1 with spaces/src1.c',
        '${CPP} ${CFLAGS} ${CCFLAGS} ${_CCCOMCOM} -c -o ${TARGET} ${SOURCES}')




# These examples are not escaped / quoted properly for CPPPATH when one of the directories has a space in

def example4():
    # Builder using a string
    # No quoting for CPPPATH in ${_CCCOMCOM}
    bld = env.Builder(
        action='${CPP} ${CFLAGS} ${CCFLAGS} ${_CCCOMCOM} -c -o ${TARGET} ${SOURCES}')
    env.AppendUnique(BUILDERS={'Example4': bld})
    env.Example4('src1.o', '../src1 with spaces/src1.c')

def example5():
    # This would work if we used SCons.Action.Action instead
    bld = env.Builder(
        action=env.Action('${CPP} ${CFLAGS} ${CCFLAGS} ${_CCCOMCOM} -c -o ${TARGET} ${SOURCES}'))
    env.AppendUnique(BUILDERS={'Example5': bld})
    env.Example5('src1.o', '../src1 with spaces/src1.c')


def example6():
    # This wont pick up on target or source, or escape CPPPATH
    bld = env.Builder(action=__Build_example6)
    env.AppendUnique(BUILDERS={'Example6': bld})
    env.Example6('src1.o', '../src1 with spaces/src1.c')

def __Build_example6(target, source, env):
    act = env.Action('${CPP} ${CFLAGS} ${CCFLAGS} ${_CCCOMCOM} -c -o ${TARGET} ${SOURCES}')
    env.Execute(act)


def example7():
    # This wiil pickup on target or source, but not escape CPPPATH
    bld = env.Builder(action=__Build_example7)
    env.AppendUnique(BUILDERS={'Example7': bld})
    env.Example7('src1.o', '../src1 with spaces/src1.c')

def __Build_example7(target, source, env):
    tststr = env.subst('${CPP} ${CFLAGS} ${CCFLAGS} ${_CCCOMCOM} -c -o ${TARGET} ${SOURCES}',
        source=source, target=target)
    env.Execute(tststr)


example5()
