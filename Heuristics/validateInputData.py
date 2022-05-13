from AMMMGlobals import AMMMException


# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all input parameters were found
        for paramName in ['m', 'n', 'S']:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Input Data' % str(paramName))

        # Validate n
        sizeCode = data.m
        if not isinstance(sizeCode, int) or (sizeCode <= 0):
            raise AMMMException('m(%s) has to be a positive integer value.' % str(sizeCode))

        # Validate m
        numCodes = data.n
        if not isinstance(numCodes, int) or (numCodes <= 0):
            raise AMMMException('n(%s) has to be a positive integer value.' % str(numCodes))

        # Validate S
        sequenceLength = 0
        for index, row in enumerate(data.S):
            data.S[index] = list(row)
            sequenceLength += len(data.S[index])
        if sequenceLength != sizeCode * numCodes:
            raise AMMMException('Size of S(%d) does not match with value of m(%d) * n(%d).' % (sequenceLength, sizeCode, numCodes))

        for value in data.S:
            for v in value:
                if not isinstance(v, int) or (v < 0) or (v > 1):
                    raise AMMMException('Invalid parameter value(%s) in S. Should be an integer equal to 1 or 0.' % str(v))
