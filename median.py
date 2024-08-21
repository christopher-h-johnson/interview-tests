import heapq
from random import randrange, randint
from statistics import median
from unittest import TestCase


class Job:
    """
    A job represents a job of an individual. We assume all jobs
    start from 2008-01


    Fields are encoded as integers.

    Encoding of time is as follows at the month level
    Jan 2008, Feb 2008, March 2008, ....
    0       , 1       , 2         , ...

    Encoding of salary:
    0 - Salary between [0, 1000)
    1 - Salary between [1000, 2000)
    ...

    Thus, all fields  are integers with the following ranges

    start, end are in the range [0, 200]
    salary is in the range [0, 1000]
    """

    def __init__(self, start: int, end: int, salary: int):
        self.start = start
        self.end = end
        self.salary = salary


class MedianFinder:
    """
    We need to find and update the data structure.

    This keeps a track of the median values over time. Note that we track
    months as integers, so this can be represented as an array
    """

    def __init__(self):
        self.medians = [0.0 for _ in range(200)]
        self.jobs_per_month = dict.fromkeys(range(0, 200))

    def create(self, jobs: list[Job]):
        """
        Here we assume we're creating the data structure for the first time

        and the list of jobs can be very big. len(jobs) >= 300 million
        """
        for j in jobs:
            for m in range(j.start, j.end + 1):
                if self.jobs_per_month.get(m) is not None:
                    self.jobs_per_month[m].append(j.salary)
                else:
                    self.jobs_per_month[m] = [j.salary]

        for k in self.jobs_per_month:
            if self.jobs_per_month.get(k) is not None:
                mid = len(self.jobs_per_month[k]) // 2
                if mid is not None:
                    if len(self.jobs_per_month[k]) % 2 == 0:
                        self.medians[k] = (heapq.nlargest(mid, self.jobs_per_month[k])[-1]
                                           + heapq.nsmallest(mid, self.jobs_per_month[k])[-1]) / 2
                    else:
                        self.medians[k] = heapq.nlargest(mid + 1, self.jobs_per_month[k])[-1]
        print(self.jobs_per_month)
        pass

    def update(self, jobs: list[Job]):
        """
        Here we assume we're just updating the data structure as new jobs
        are ingested / discovered

        and here the list of jobs can be in the range of 100k-1million
        """
        self.create(jobs)
        pass


def get_random_jobs(total_count: int, max_salary: int):
    jobs = []
    for i in range(total_count):
        start = randint(0, 5)
        end = randint(start, 10)
        salary = randrange(25000, max_salary)
        job = Job(start=start, end=end, salary=salary)
        jobs.append(job)
    return jobs


def checkEqual(l1, l2):
    if sorted(l1) == sorted(l2):
        return True
    else:
        return False


class Test(TestCase):
    def test_create_median(self):
        jobs = get_random_jobs(20, 150000)
        mf = MedianFinder()
        mf.create(jobs=jobs)
        self.assertEqual(median(mf.jobs_per_month[0]), mf.medians[0])

    def test_create_and_update_median(self):
        jobs = get_random_jobs(20, 150000)
        mf = MedianFinder()
        mf.create(jobs=jobs)
        print(mf.medians)
        mf2 = MedianFinder()
        jobs_to_update = get_random_jobs(20, 100000)
        mf2.jobs_per_month = mf.jobs_per_month
        mf2.update(jobs=jobs_to_update)
        print(mf2.medians)
        self.assertFalse(checkEqual(mf.medians, mf2.medians))
        self.assertEqual(median(mf2.jobs_per_month[0]), mf2.medians[0])
