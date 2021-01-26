# // Copyright (c) 2012 Sutoiku, Inc. (MIT License)

# // Some algorithms have been ported from Apache OpenOffice:

# /**************************************************************
#  *
#  * Licensed to the Apache Software Foundation (ASF) under one
#  * or more contributor license agreements.  See the NOTICE file
#  * distributed with this work for additional information
#  * regarding copyright ownership.  The ASF licenses this file
#  * to you under the Apache License, Version 2.0 (the
#  * "License"); you may not use this file except in compliance
#  * with the License.  You may obtain a copy of the License at
#  *
#  *   http://www.apache.org/licenses/LICENSE-2.0
#  *
#  * Unless required by applicable law or agreed to in writing,
#  * software distributed under the License is distributed on an
#  * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  * KIND, either express or implied.  See the License for the
#  * specific language governing permissions and limitations
#  * under the License.
#  *
#  *************************************************************/


def years_between_dates(date1, date2):
    delta = date2 - date1
    return (delta.days / 365)


# // Credits: algorithm inspired by Apache OpenOffice
# // Calculates the resulting amount
def irrResult(values, dates, rate):
    r = rate + 1
    result = values[0]
    for i in range(1, len(values)):
        result = result + values[i] / pow(r, years_between_dates(dates[0], dates[i]))
        i = i + 1
    return result


# // Calculates the first derivation
def irrResultDeriv(values, dates, rate):
    r = rate + 1
    result = 0
    for i in range(1, len(values)):
        frac = years_between_dates(dates[0], dates[i])
        result = result - frac * values[i] / pow(r, frac + 1)
        i = i + 1
    return result


def xirr(values, dates):
    # // Check that values contains at least one positive value and one negative value
    positive = False
    negative = False
    for v in values:
        if v > 0:
            positive = True
        if v < 0:
            negative = True

    # // Return error if values does not contain at least one positive value and one negative value
    if not (positive and negative):
        return 'Error'
    # // Initialize guess and resultRate
    guess = 0.1
    resultRate = guess

    # // Set maximum epsilon for end of iteration
    epsMax = 1e-10

    # // Set maximum number of iterations
    iterMax = 20

    # // Implement Newton's method
    iteration = 0
    contLoop = True
    while contLoop and (iteration < iterMax):
        resultValue = irrResult(values, dates, resultRate)
        newRate = resultRate - (resultValue / irrResultDeriv(values, dates, resultRate))
        epsRate = abs(newRate - resultRate)
        resultRate = newRate
        if resultRate < -1:
            resultRate = -0.999999999
        contLoop = (epsRate > epsMax) and (abs(resultValue) > epsMax)
        iteration = iteration + 1
    if contLoop:
        return epsRate > epsMax, epsRate, 'iterMax'
    return resultRate