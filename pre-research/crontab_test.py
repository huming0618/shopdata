from crontab import CronTab
cron = CronTab()
job = cron.new(command='echo date >> ls.txt')

job.minute.during(5, 50).every(1)
cron.run_scheduler()
