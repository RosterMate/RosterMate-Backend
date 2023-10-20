from calendar import monthrange

class Scheduler:
    def __init__(self, doctors_details, shift_types, num_doctors,consecutive_shifts, year, month):
        self.doctors_details = doctors_details  # doctor details list - [doctor id, next are date with shifts that he/she want a leave]
        self.shift_types = shift_types          # shift types in the respective ward
        self.num_doctors = num_doctors          # number of doctors need per each shift
        self.consecutive_shifts = consecutive_shifts
        self.year = int(year)       # int
        self.month = int(month)     # int
        self.assignment = {}        # assignment = {doctor id: [(date, shift), (date, shift), ...], ...}

    def is_a_leave(self, date1, shift, date2, leaves):
        if date1 == date2 and shift in leaves:
            return True
        return False

    def candidate_doctors(self,date,shift_number, shifts_per_doc_count):
        # return candidate doctor IDs for a shift
        candidates = []

        # details of doctors - [doctor id, next are date with shifts that he/she want a leave]
        #                                - [date, shift1, shift2, ...],[date, shift1, shift2, ...]
        #                                - shift1, shift2, ... are the shifts that doctor want a leave

        other_doctors = []
        for doc in self.doctors_details:

            for d in doc[1:]:
                if self.is_a_leave(date,self.shift_types[shift_number], d[0], d[1:]):
                    #print('Doctor id =',doc[0],'Date =',date,'Shift =',self.shift_types[shift_number])
                    break
            else:

                if len(self.assignment[doc[0]]) >= shifts_per_doc_count+self.consecutive_shifts:
                    other_doctors.append(doc[0])
                    continue
                self.assignment[doc[0]].append((date,self.shift_types[shift_number]))
                candidates.append(doc[0])

                if self.num_doctors[self.shift_types[shift_number]] == len(candidates):
                    break

        #random.shuffle(candidates)

        while self.num_doctors[self.shift_types[shift_number]] != len(candidates) and len(other_doctors) != 0:
            candidates.append(other_doctors.pop())
        
        if self.num_doctors[self.shift_types[shift_number]] != len(candidates):
            print("Need",self.num_doctors[self.shift_types[shift_number]] - len(candidates),"more doctors for",self.shift_types[shift_number],"shift on",date )
            #return -1
        
        return candidates

    def calculate_shifts_per_doc(self):
        count = min([len(self.assignment[key]) for key in self.assignment])

        return count

    def get_schedule_with_equal_shifts(self):
        
        first_day, self.num_days = monthrange(self.year, self.month)

        #num_doctors_per_day = sum([self.num_doctors[i] for i in self.shift_types])
        #total_shifts_in_a_month = self.num_days * num_doctors_per_day
        #print("total_shifts_in_a_month =", total_shifts_in_a_month)
        #maximum_shifts_for_a_doctor = total_shifts_in_a_month//len(self.doctors_details)
        #print("maximum_shifts_for_a_doctor =", maximum_shifts_for_a_doctor)

        shifts = []
        # shifts = [ [date 1, shift 1, shift 2, shift 2], ...]
        #             shift 1 = [doctor id 1, doctor id 2, ...]
        #             shift 2 = [doctor id 1, doctor id 2, ...]

        for i in range(1, self.num_days+1):
            str_month = str(self.month)
            str_day = str(i)
            if len(str_month) == 1:
                str_month = str_month
            if len(str_day) == 1:
                str_day = str_day
            date = str(self.year) + "-" + str_month + "-" + str_day

            shift = [date]
            for i in self.shift_types:
                shift.append(-1)
            shifts.append(shift)

        for doctor_detail in self.doctors_details:
            self.assignment[doctor_detail[0]] = []

        # shifts = [ [date 1, shift 1, shift 2, shift 3], ...]
        #             shift 1 = [doctor id 1, doctor id 2]
        #             shift 2 = [doctor id 1, doctor id 2, ...]

        #number_of_doctors = len(self.doctors_details)

        shifts_per_doc_count = 0

        for date in range(self.num_days):
            for shift_number in range(1, len(self.shift_types)+1):

                if shifts[date][shift_number] == -1:
                    candidates = self.candidate_doctors(shifts[date][0],shift_number-1, shifts_per_doc_count)
                    shifts[date][shift_number] = candidates
                    shifts_per_doc_count = self.calculate_shifts_per_doc()
                    
        #print('assignment =',self.assignment)
        #print('Assignment =>')
        #for key in self.assignment:
        #    print('doctor id:',key,'|',len(self.assignment[key]),':',self.assignment[key])
        #    print()

        #return shifts
        return self.assignment
        
if __name__ == "__main__":

    # details of doctors - [doctor id, next are date with shifts that he/she want a leave]
    #                       [date, shift1, shift2, ...] - shift1, shift2, ... are the shifts that doctor want a leave
    doctors_details = [
        ["1", ["2023-10-1", "morning","evening", "night"], ["2023-10-23", "evening", "night"]],
        ["2", ["2023-10-3", "evening"], ["2023-10-8", "morning", "night"]],
        ["3", ["2023-10-9", "night"], ["2023-10-20", "evening", "night"]],
        ["4", ["2023-10-12", "evening"], ["2023-10-18", "morning", "night"]],
        ["5", ["2023-10-7", "evening"], ["2023-10-29", "evening", "night"]],
        ["6", ["2023-10-6", "evening"], ["2023-10-18", "morning", "night"]],
        ["7", ["2023-10-29", "morning","evening"], ["2023-10-13", "evening", "night"]],
        ["8", ["2023-10-13", "night"], ["2023-10-26", "morning", "night"]],
    ]

    shift_types = ["morning", "evening", "night"] # shift types
    num_doctors = {"morning": 4, "evening": 5, "night": 2} # number of doctors need for each shift
    consecutive_shifts = 2 # consecutive shifts that can do consecutively

    year = 2023
    month = 10

    scheduler = Scheduler(doctors_details, shift_types, num_doctors,consecutive_shifts, year, month)
    print(scheduler.get_schedule_with_equal_shifts())
