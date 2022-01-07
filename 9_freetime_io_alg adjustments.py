
students = []

class Student:
    def __init__(self, name, schedule, day_start = 8.5, day_end = 19) :
        #schedule is a dictionary
        self.name = name
        self.schedule = schedule
        self.begin = day_start
        self.end = day_end
        self.freetime = freetime(self)

def freetime(student) :
    freetime_dict = {}
    
    for day in student.schedule :
        free_list = []
        course_times = student.schedule[day]
        #next line appends a 'course' that is (day_end, None)
        course_times.append((student.end, None))
        
        for i in range(len(course_times)-1) :
            earlier_end = course_times[i][1]
            later_start = course_times[i+1][0]

            if earlier_end < later_start :
                free_list.append((earlier_end, later_start))
        freetime_dict.update([(day, free_list)])

    return freetime_dict

def float_range(start, stop, step = .25) :
    range_list = []
    i = start
    while i <= stop :
        range_list.append(i)
        i += step
    return range_list

def overlap(student, other_student) :
    overlap_dict = {}
    for day in student.freetime :
        overlap_list = []
        a = student.freetime[day] #student
        b = other_student.freetime[day] #student from student list
            #^that's a whole list of tuples (freetimes)
                
        overall_a = []
        overall_b = []
                
        for value in a :
        #ie for tuple in list of tuples
            overall_a.extend(float_range(value[0], value[1]))
        for value in b :
            overall_b.extend(float_range(value[0], value[1]))

        if len(overall_a) > 0 :
            prev_time = overall_a[0]

        for time in overall_a:
            if time in overall_b:
                if len(overlap_list) == 0 :
                    overlap_list.append((time,))
                else : 
                    if time > (prev_time + .25) :
                        overlap_list[-1] = overlap_list[-1] + (prev_time,)
                        #^ fancy way to append to a tuple
                        overlap_list.append((time,))
                        #^it doesn't assume an end to your day
                prev_time = time
            
        overlap_dict.update([(day, overlap_list)])
    return overlap_dict

def time_conversion_forward (time) :
    #float time to time-representation
    hours = int(time)
    if hours > 12 :
        hours = hours - 12
    minutes = (time*60) % 60
    return "%d:%02d" % (hours, minutes)

def time_conversion_backward (time) :
    #this requires times as army-time numbers
    #print(time)
    hour = time.split(':')[0]
    minute = int(time.split(':')[1])

    if minute == 0 :
        new_min = '.0'
    elif minute <= 15 :
        new_min = '.25'
    elif minute <=30 :
        new_min = '.5'
    else :
        new_min = '.75'

    return float(hour + new_min)

def print_overlap(student, other_student) :
    the_dict = overlap(student, other_student)
    print(student.name.capitalize(), 'and', other_student.name.upper(), "are both free:")
    
    for day in the_dict : 
        print("{:>9}".format(day), ':', end = ' ')
        #this is a kind of complicated way to do time-conversions,
        # it involves printing each bit by bit
        for tup in the_dict[day] :
            print('(', end = '')
            for i in range(len(tup)) : #because sometimes just one num
                print(time_conversion_forward(tup[i]), end = '')
                if i == 0 :
                    print(', ', end = '')
            print(') ', end = '')
        print()
    return None


def create_student(filename, student_dict) :
    import os
    path = os.path.join(filename)
    f = open(path, 'r') #open as read-only

    schedule_dict = {}
    student_name = f.readline().strip().lower() #+ '.txt'
    all_lines = f.readlines()
    i = 0
    while i < len(all_lines) :
        if all_lines[i] == '\n':
            i +=1
            the_day = all_lines[i].strip()
            classes_on_day = []
            i += 1
            while  i < len(all_lines) and all_lines[i] != '\n'  :
                single_class = all_lines[i].strip()
                i+=1
                beg_time = time_conversion_backward(single_class.split(',')[0].strip())
                end_time = time_conversion_backward(single_class.split(',')[1].strip())
                #remember those are still strings in the tuple of 'class times'
                classes_on_day.append((beg_time, end_time))
            schedule_dict[the_day] = classes_on_day

    #Finally, create the student
    student_dict[student_name] = Student(student_name, schedule_dict)
    return None

def make_students(student_names_dict) :
    #print(student_names_dict.keys())
    for person in student_names_dict.keys() :
        create_student('student_schedules/' + person +'.txt', student_names_dict)



#######################################################################################
#######################################################################################

print()
print()
user_name = input("Who's schedule would you like to compare? ").lower()

try :
    import os
    filename = user_name.lower() + '.txt'
    path = os.path.join('student_schedules')
    #make the list of other students available:
    files = os.listdir(path)
    #create a dictionary of those student names so you can assign
    # the instance of the student class as the value later on

    student_dict = {}
    for name in files : 
        student_dict[name[:-4]] = 'woohoo! empty!' #getting rid of the .txt to get names

    path = os.path.join('student_schedules/' + filename)
    f = open(path, 'r')
    #if this isn't working, you need to change directory in terminal to
    # where this file is stored.

    make_students(student_dict)

    for student in student_dict.keys() : 
        if student_dict[student].name != user_name :
            print()
            print_overlap(student_dict[user_name], student_dict[student])

except FileNotFoundError: 
    print("Name not found. Please make sure your schedule is in the folder and try again.")
except Exception as e :
    print('Something else went wrong:')
    print(e)

#name_to_check = input("Who's schedule would you like to compare? ")
#for student in students : 
#    if student.name == name_to_check :
#        print()
#        print_overlap(student)
#print()
#print("(if your schedule-overlap wasn't printed, you may have given faulty input)")