import os
import random
from AMMMGlobals import AMMMException
from itertools import chain


class InstanceGenerator(object):
    # Generate instances based on read configuration.

    def __init__(self, config):
        self.config = config

    def generate(self):
        # load config parameters
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        sizeCode = self.config.sizeCode
        numCodes = self.config.numCodes

        if not os.path.isdir(instancesDirectory):
            raise AMMMException('Directory(%s) does not exist' % instancesDirectory)

        for i in range(numInstances):
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            fInstance = open(instancePath, 'w')

            # Calculate set S
            codeSequence = [[0 for _ in range(sizeCode)] for _ in range(numCodes)]
            hashmap = {}
            for j in range(numCodes):
                hasRepeated = True
                for k in range(sizeCode):
                    if j == 0:
                        # sequence starts always with all zeros code
                        codeSequence[j][k] = 0
                    else:
                        codeSequence[j][k] = random.randint(0, 1)
                    if k == sizeCode-1:
                        hashmap[j] = codeSequence[j]
                        while hasRepeated:
                            # find if actual row is equal to any previous row
                            repeated = self.getRepeatedCodes(hashmap)
                            if len(repeated) > 0:
                                # duplication found
                                # re-do the entire duplicated row
                                repeated.pop()
                                key = repeated.pop()
                                for r in range(sizeCode):
                                    codeSequence[key][r] = random.randint(0, 1)
                                    if r == sizeCode - 1:
                                        hashmap[key] = codeSequence[key]
                            else:
                                hasRepeated = False

            # print .dat file
            fInstance.write('m=%d;\n' % sizeCode)
            fInstance.write('n=%d;\n' % numCodes)
            fInstance.write('S =\n[\n')

            for j in range(numCodes):
                fInstance.write('  [')
                for k in range(sizeCode):
                    fInstance.write(' %d' % codeSequence[j][k])
                    if k == sizeCode - 1:
                        fInstance.write(' ]\n')

            fInstance.write('];\n')
            fInstance.close()

    def getRepeatedCodes(self, hashmap):
        # Perform a search on a reverse map to detect duplicate codes
        reverseMap = {}
        for key, value in hashmap.items():
            reverseMap.setdefault(tuple(value), set()).add(key)

        res = set(chain.from_iterable(values for key, values in reverseMap.items() if len(values) > 1))
        return res

