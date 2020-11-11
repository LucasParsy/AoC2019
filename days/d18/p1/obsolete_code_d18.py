    def path_key(self, pos: Point, searchedPos: Point,
                    prevPoint: Point = badPoint,
                    doors: List[str] = [], path: List[Point] = [],
                    res: Path = badPath) -> Path:
        for dir in self.directions:
            nextPoint = pos + dir
            # print(res.distance)
            distPoint = nextPoint - searchedPos
            manhattan = abs(distPoint.x) + abs(distPoint.y)
            #print(len(path)+ manhattan + 1)
            if len(path) + manhattan + 1 >= res.distance:
                return res
            if nextPoint == prevPoint:
                continue
            c = self.getPoint(nextPoint)
            if c in self.wallsChar:
                continue
            if nextPoint == searchedPos:
                foundPath = path + [dir]
                #print("solution found!", len(foundPath))
                return Path(len(foundPath), foundPath, doors)

            if ord(c) in range(ord('A'), ord('Z')+1):
                doors = doors + [chr(ord(c)+32)]

            nRes = self.path_key(nextPoint, searchedPos, pos, doors,
                                 path + [dir], res)
            if nRes.distance < res.distance:
                res = nRes
        return res


def find_shortest_theoric(self, combis: Combinations, currPoint: str,
                              pathLen: int, keys: List[str], solution: Path) -> int:
        if pathLen > solution.distance or len(keys) == self.numKeys:
            return pathLen
        poss = combis[currPoint]
        for nKey, nPath in poss.items():
            if nKey in keys:  # or any (x not in keys for x in nPath.doors):
                continue
            return self.find_shortest_theoric(combis, nKey, pathLen + nPath.distance, keys + [nKey], solution)

    def find_best_path(self, combis: Combinations, currPoint: str,
                       keys: List[str], pathLen: int, solution: Path) -> Path:
        shortest = self.find_shortest_theoric(
            combis, currPoint, pathLen, keys, solution)
        if shortest > solution.distance:
            return solution
        if len(keys) == self.numKeys:
            print("found keys path solution:", pathLen)
            return Path(pathLen, [], keys)

        poss = combis[currPoint]
        for nKey, nPath in poss.items():
            if nKey in keys or any(x not in keys for x in nPath.doors):
                continue
            nSol = self.find_best_path(
                combis, nKey, keys + [nKey], pathLen + nPath.distance, solution)
            if nSol.distance < solution.distance:
                solution = nSol
        return solution


    def optimizeKeyPathCombinations(self, combis: Combinations) -> List[Point]:
        print("test combinations")
        self.badPath = Path(999999, [], [])

        res = []
        times = []
        numTries = 1
        for _ in range(numTries):
            start = datetime.now()
            res = self.find_best_path(combis, "start", [], 0, self.badPath)
            end = datetime.now()
            times.append((end-start).total_seconds())
        print("done in average", sum(times) / numTries, "secs")
        print(times)
        print(res.distance, res.doors)
        res.path = self.getPathFromStrPath(combis, res.doors)
        # print(path)
        f = open("final_path.py", 'w')
        f.write(str(res))
        return res.path

    def path_map(self, prevPoint: Point, pos: Point, keys: List[str], path: List[Point]) -> List[Point]:
        res = []
        #print(len(path), path)
        for dir in self.directions:
            nextPoint = pos + dir
            if len(path)+1 >= self.shortestSol:
                return []
            if nextPoint == prevPoint:
                continue
            c = self.getPoint(nextPoint)
            if c == '#':
                continue
            # print(alreadyTaken)
            if ord(c) in range(ord('a'), ord('z')+1) and c not in keys:
                if len(keys) == self.numKeys - 1:
                    self.shortestSol = len(path)+1
                    print("SOLUTION FOUND!", len(path)+1)
                    return path + [dir]
                nRes = self.path_map(
                    Point(-42, -42), nextPoint, keys + [c], path + [dir])
            elif ord(c) in range(ord('A'), ord('Z')+1) and chr(ord(c)+32) not in keys:
                return []
            else:
                nRes = self.path_map(pos, nextPoint, keys, path + [dir])
            if nRes and (len(nRes) < len(res) or not res):
                res = nRes
        return res



    def getRecursiveDependency(self, requiredKeys: Dict(str, List(str)), index: str, res: List[str]):
        for elem in requiredKeys[index]:
            if elem not in res:
                res.append(elem)
            self.getRecursiveDependency(requiredKeys, elem, res)

    def getRequiredKeys(self, combis: Combinations) -> Dict(str, List[str]):
        requiredKeys = {}
        for p1 in combis.keys():
            if p1 == 'start':
                continue
            foundKeys = []
            foundKeys.append(combis['start'][p1].doors)
            requiredKeys[p1] = list(set.intersection(
                *[set(list) for list in foundKeys]))

        for elem in requiredKeys.keys():
            self.getRecursiveDependency(requiredKeys, elem, requiredKeys[elem])
        #requiredKeys = {k: v for k, v in sorted(requiredKeys.items(), key=lambda item: combis['start'][item[0]].distance)}
        requiredKeys = {k: v for k, v in sorted(
            requiredKeys.items(), key=lambda item: len(item[1]), reverse=True) }
        print(requiredKeys)
        return requiredKeys

    def appendKeyToSolution(self,
                            combis: Combinations,
                            requiredKeys: Dict(str, List[str]),
                            nKey: str,
                            solution: List[str]) -> List[str]:
        if len(solution) == 1:
            solution.append(nKey)
            return (solution, combis['start'][nKey].distance)
        startIndex = 0
        if requiredKeys[nKey]:
            indexes = [solution.index(i)
                       for i in requiredKeys[nKey] if i in solution]
            if indexes:
                startIndex = max(indexes)
        lastIndex = len(solution)-1

        needed = [solution.index(x)
                  for x in solution[1:] if nKey in requiredKeys[x]]
        if needed:
            lastIndex = min(needed) - 1
            if lastIndex > len(solution)-2:
                lastIndex += 1

        distances = [-combis[solution[x]][solution[x+1]].distance +
                     combis[solution[x]][nKey].distance +
                     combis[nKey][solution[x+1]].distance
                     for x in range(startIndex, lastIndex)]

        if lastIndex == len(solution)-1:
            distances.append(combis[solution[lastIndex]][nKey].distance)
        ind = 0
        if distances:
            minDist = min(distances)
            ind = distances.index(minDist)
        else:
            minDist = (-combis[solution[startIndex]][solution[startIndex+1]].distance +
                       combis[solution[startIndex]][nKey].distance +
                       combis[nKey][solution[startIndex+1]].distance)

            combis[solution[startIndex]][nKey].distance
        ind += 1 + startIndex
        solution.insert(ind, nKey)
        return (solution, minDist)

    def tryRecombinations(self, combis: Combinations, requiredKeys:  Dict(str, List[str]),
                            solution: List[str], dist: int) -> int:
        solCopy = copy(solution[1:])
        isStable = False
        while isStable == False:
            isStable = True
            for char in solCopy:
                distWithoutChar = dist
                ind = solution.index(char)
                if ind == len(solution)-1:
                    distWithoutChar -= combis[solution[ind-1]][solution[ind]].distance
                else:
                    distWithoutChar -= (combis[solution[ind-1]][solution[ind]].distance +
                                        combis[solution[ind]][solution[ind+1]].distance -
                                        combis[solution[ind-1]][solution[ind+1]].distance)

                solWithoutChar = copy(solution)
                solWithoutChar.remove(char)
                _, nDist = self.appendKeyToSolution(
                combis, requiredKeys, char, solWithoutChar)
                distWithoutChar  += nDist
                if distWithoutChar < dist:
                    dist = distWithoutChar
                    solution = solWithoutChar
                    isStable = False
                    break

        return dist

    def tryFastSolution(self, combis: Combinations) -> List[Point]:
        solution = ['start']
        requiredKeys = self.getRequiredKeys(combis)

        dist = 0
        for nKey in requiredKeys.keys():
            _, nDist = self.appendKeyToSolution(
                combis, requiredKeys, nKey, solution)            
            dist += nDist
            #self.tryRecombinations(combis, requiredKeys, solution, dist)
 

        print()
        print(solution)
        print("dist:", dist)
        return self.getPathFromStrPath(combis, solution[1:])

        for sizeFreebie in range(len(list(requiredKeys.items())[0][1])-1, -1, -1):
            print("size freebie:", sizeFreebie)
            freebies = [x[0]
                        for x in requiredKeys.items() if len(x[1]) == sizeFreebie]
            #freebies = [x[0] for x in requiredKeys.items()]

            iters = list(itertools.permutations(freebies))
            #iters.reverse()
            solWithoutFreebies = copy(solution)
            for elem in freebies:
                solWithoutFreebies.remove(elem)
            totalDistance = self.getDistanceFromStrPath(combis, solution[1:])
            distFreebies = self.getDistanceFromStrPath(
                combis, solWithoutFreebies[1:])

            print("\n\n")

            numTries = len(iters)
            for i, it in enumerate(iters):
                if i % 10000 == 0:
                    print(i / numTries, end="\r")
                nSol = copy(solWithoutFreebies)
                nDist = distFreebies
                for char in it:
                    nSol, distAdd = self.appendKeyToSolution(
                        combis, requiredKeys, char, nSol)
                    nDist += distAdd
                    if nDist >= totalDistance:
                        break
                if nDist < totalDistance:
                    print("\n", totalDistance, '\n')
                    solution = nSol
                    totalDistance = nDist

        print("\n\n")
        print(solution)
        print(self.getDistanceFromStrPath(combis, solution[1:]))
        return self.getPathFromStrPath(combis, solution[1:])
