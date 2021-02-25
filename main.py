from collections import defaultdict


def batches(l):
    for i in range(len(l) - 1):
        yield l[i:i + 2]


class Solution:
    def __init__(self) -> None:
        super().__init__()
        self.data = None
        self.input_file_name = './input/e.txt'
        self.output_file_name = 'output.txt'
        self.STREETS = {}
        self.CARS = {}
        self.STREET_LENGTHS = {}
        self.DURATION = None
        self.NUM_OF_INTERSECTION = None
        self.NUM_OF_STREETS = None
        self.NUM_OF_CARS = None
        self.BONUS = None
        self.BestCarInStreet = {}

    def readingInput(self, file_name):
        with open(file_name) as f:
            self.data = [i.strip() for i in f.readlines()]
            line_num = 0
            self.DURATION, self.NUM_OF_INTERSECTION, self.NUM_OF_STREETS, self.NUM_OF_CARS, self.BONUS = map(int, self.data[0].split(' '))
            for _ in range(self.NUM_OF_STREETS):
                line_num += 1
                line = self.data[line_num]
                START, END, NAME, LEN = line.split(' ')
                self.STREETS[NAME] = {'start': int(START), 'end': int(END), 'len': int(LEN)}
                self.STREET_LENGTHS[NAME] = int(LEN)

            for i in range(self.NUM_OF_CARS):
                line_num += 1
                line = self.data[line_num]
                CAR_STREETS = line.split(' ')[1:]
                self.CARS[i] = list(CAR_STREETS)

    def lengthOfPath(self, path):
        scores = 0
        for street in path[1:]:
            scores += 1 + self.STREET_LENGTHS[street]
        return scores

    def run(self):
        self.readingInput(self.input_file_name)
        for key, streets in self.CARS.items():
            pathLen = self.lengthOfPath(streets)
            if pathLen <= self.DURATION:
                self.BestCarInStreet[key] = pathLen

        BEST_CARS = sorted(self.BestCarInStreet, key=self.BestCarInStreet.get)

        streetIntersectMAP = {}
        startStreet = defaultdict(list)
        endStreet = defaultdict(list)
        for slowStreet, data in self.STREETS.items():
            startStreet[data['start']].append(slowStreet)
        for slowStreet, data in self.STREETS.items():
            endStreet[data['end']].append(slowStreet)

        for slowStreet, data in self.STREETS.items():
            for streetTwo in startStreet[data['end']]:
                streetIntersectMAP[f'{slowStreet}__{streetTwo}'] = data['end']

        perfectIntersection = defaultdict(lambda: 0)
        streetsWithID = defaultdict(set)

        for carID in BEST_CARS:
            availableStreets = self.CARS[carID]
            for elements in batches(availableStreets):
                streetOne, streetTwo = elements
                intersectID = streetIntersectMAP[f'{streetOne}__{streetTwo}']
                perfectIntersection[f'{streetOne}__{intersectID}'] += 1
                streetsWithID[intersectID].add(streetOne)

        dResult = {}
        for CAR_ID in BEST_CARS:
            availableStreets = self.CARS[CAR_ID]
            for STREET in availableStreets:
                street = self.STREETS[STREET]
                dResult[street['end']] = {STREET: 1}

        results = []
        results.append(str(len(dResult)))
        for intersectID, streets in dResult.items():
            results.append(str(intersectID))
            results.append(str(len(streets)))
            for street_name, seconds in streets.items():
                results.append(f'{street_name} {seconds}')
        with open(self.output_file_name, 'w') as f:
            f.writelines('\n'.join(results))


answer = Solution()
answer.run()
