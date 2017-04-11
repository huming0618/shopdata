#coding=utf8
import argparse
import datetime

from gevent import monkey; monkey.patch_all()
import gevent

from DaySaleTask import DaySaleTask



def run_subtasks(tasks):
    gevent.joinall(tasks)
    # checkt the status of the tasks
    failed = [x for x in tasks if x.successful() is False]
    print "Failed %d" % len(failed)
    for task in tasks:
        print 'successful %s' % (task.successful())

def run(date_1, date_2):

    DIVIDER = 30

    from datetime import datetime
    from datetime import timedelta
    try:
        from_date = datetime.strptime(date_1, "%Y-%m-%d")
        to_date = datetime.strptime(date_2, "%Y-%m-%d")
    except ValueError as e:
        print "Invalid format of the date"

    if from_date > to_date:
        from_date,to_date = to_date,from_date

    days = (to_date - from_date).days

    start_date = from_date
    end_date = to_date

    points = range(0, days, DIVIDER)
    segments = []
    for x in points:
        print days, x
        end_date = start_date + timedelta(days=DIVIDER)
        if end_date > to_date:
            end_date = to_date
        segments.append((start_date, end_date))
        start_date = end_date + timedelta(days=1)

    def create_subtask(item):
        day1 = item[0].strftime("%Y%m%d")
        day2 = item[1].strftime("%Y%m%d")
        print day1, day2
        def run_subtask():
            task1 = DaySaleTask()
            task1.run({'from': day1, 'to': day2})
        return gevent.spawn(run_subtask)

    task_list = map(create_subtask, segments)
    run_subtasks(task_list);

    print len(DaySaleTask.records)
    print "DONE"

    # print segments


#python run.py --from 2016-01-01 --to 2016-12-18
if __name__=='__main__':

    # gevent_test()
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="start")
    parser.add_argument("--to", dest="end")
    arg = parser.parse_args()

    # print arg, type(arg)
    run(arg.start, arg.end)
    # option = {'from': arg.start, 'to': arg.end}
    # # print option
    #
    # task = DaySaleTask()
    # task.run(option)
