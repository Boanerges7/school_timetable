import pathlib
import csv


# Let's start by defines variables
subjects_list = []
start_hour = 8 # school start at 8.am
next_hour = 9 # 1rst next hour is 9.am
school_days = [
	'monday',
	'tuesday'
]
time_slot_list = [] # get list of time slot
subject_per_slot = {}
MAX_HOUR_PER_SUBJECT = 6 # use capital letter because it's a constant variable
subject_hour_count = {}


# 1rst method
# def fill_in_subjects_list():
# 	"""Ask user subjects and fill in subjects list"""

# 	enter_another_subject = True

# 	while enter_another_subject:
# 		subject = input('Type another subject: ')
# 		subject = subject.capitalize()

# 		if not subject in subjects_list:
# 			subjects_list.append(subject)
# 			subject_hour_count[subject] = MAX_HOUR_PER_SUBJECT
# 		else:
# 			print(f'You\'ve already type {subject} in list.')

# 		question = input('Enter another subject (type "n" to exit)?')

# 		if question.lower() == 'n':
# 			enter_another_subject = False

# 2nd method
def fill_out_subjects_list():
	"""Ask user subjects and fill in subjects list"""

	subjects = input('Type all subjects you want add in subjects list\
and separate them by comma: ') # we collect all subjects

	the_subjects = subjects.replace(', ', ',') # remove space after comma

	# Split all subjects in order to put them into a list
	the_subjects = the_subjects.split(',')

	for subject in the_subjects:
		subject = subject.capitalize()

		if not subject in subjects_list:
			subjects_list.append(subject)
			subject_hour_count[subject] = MAX_HOUR_PER_SUBJECT

def ask_hour():
	"""Ask hour to user"""
	print(f'Subjects list: {subjects_list}')

	print(f'Planning time: {start_hour}h-{next_hour}h')
	user_answer = input('What\'s subject do you want put here? ')

	return user_answer

def fill_in_timetable():
	"""Display an hour & ask user which subject he want to put there"""
	global start_hour
	global next_hour

	for day in school_days:
		# Reset start and next hour
		the_hour = {}
		time = 0
		start_hour = 8 # we suppose that school start at 8.am
		next_hour = 9

		print('\n---------------------------')
		print(f'{day.capitalize()} timetable')
		print('---------------------------\n')

		while time < 4: # Suppose we've 4hours course/day (you can change it)

			hour_format = f'{start_hour}h-{next_hour}h' # format time slot
			# it's represent 8 hours/per day for school
			if time == 2: # if it's a midday (12.am), make a break
				# Add a break in timetable with 'Break time' as inscription
				subject_per_slot[hour_format] = ['Break time']

				# Add hour format while making sure we avoid duplicate
				if not hour_format in time_slot_list:
					time_slot_list.append('hour_format')
				
			else:
				chosen_subject = ask_hour().capitalize()
				print(f'start_hour: {start_hour}')
				print(f'next_hour: {next_hour}')

				# Check that subject chosen by user is in subjects list
				while not chosen_subject in subjects_list:
					print(f'{chosen_subject} is not in subjects list.')
					print('Choose another subject.')
					chosen_subject = ask_hour().capitalize()

				# Add hour format while making sure we avoid duplicate
				if not hour_format in time_slot_list:
					time_slot_list.append(hour_format)
					subject_per_slot[hour_format] = [chosen_subject]
				else:
					subject_per_slot[hour_format] += [chosen_subject]

				# Check that chosen subject max hours didn't reached
				for subject, max_hour in subject_hour_count.items():
					if chosen_subject == subject:
						# remove one hour on subject max hour
						subject_hour_count[chosen_subject] = max_hour - 1

			# go to next hour
			start_hour += 1
			next_hour += 1
			time += 1

# RUN THE PROGRAM

fill_out_subjects_list()
fill_in_timetable()
print(f'Subject per slot: {subject_per_slot}')

timetable_path = pathlib.Path.cwd() / 'timetable.csv'

# Now, let's write process to save timetable into a csv file
with open(timetable_path, 'w') as timetable_file:
	timetable_writing = csv.writer(timetable_file)

	# Write headers into csv file
	csv_headers = ['Hours']
	csv_headers.extend(school_days)
	timetable_writing.writerow(csv_headers)

	# Write content into csv file
	for time_slot, concerned_subjects in subject_per_slot.items():
		time_line = [time_slot]
		concerned_subjects_list = []

		if concerned_subjects == ['Break time']:
			for x in range(0, len(school_days)):
				concerned_subjects_list.append('Break time')
		else:
			concerned_subjects_list = concerned_subjects

		final_line = time_line + concerned_subjects_list
		timetable_writing.writerow(final_line)
	print('Your timetable is ready')