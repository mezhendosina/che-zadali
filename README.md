This telegram bot sends homework from [my school journal](https://sgo.edu-74.ru/). Also, they can send my class
timetable at school and class attendants for today.

## List of commands

- `/che` - sends homework for tomorrow
- `/lessons` - sends timetable
- `/pidors_today` - sends class attendants for today

## How it works

Every hour, my server sends requests to the school journal website, gets that week's homework, and stores the new
homework in a PostgreSQL table.

Every time you send a `/che` to [the bot](https://che_zadaliBot.t.me), it receives the next day's homework from the
PostgreSQL table and sends it to you.

With `/lessons`, everything is much easier. When you send this command to the bot, it opens the lessons.txt file and
sends its contents to you
