import streamlit as st
import pandas as pd


class Day:
    def __init__(self,name,p06_22,p22_24,p00_06):

        self.period1 = p06_22
        self.period2 = p22_24
        self.period3 = p00_06
        self.calculated_value = 0
        self.name = name

class Regular(Day):
    def __init__(self,name,p06_22,p22_24,p00_06):
        super().__init__(name,p06_22,p22_24,p00_06)
        self.calculated_wage = (1.25*p00_06 + 1*p06_22 + 1.25*p22_24)

    def calculate(self):
        calculation =  (1.25 * self.period3 + 1 * self.period1 + 1.25 * self.period2)
        self.calculated_wage = self.calculated_wage + calculation



class Bonus(Day):
    def __init__(self,name, p06_22, p22_24, p00_06):
        super().__init__(name,p06_22,p22_24,p00_06)
        self.calculated_wage = (2 * p00_06 + 1.75 * p06_22 + 2 * p22_24)

    def calculate(self):
        calculation = (2 * self.period3 + 1.75 * self.period1 + 2 * self.period2)
        self.calculated_wage = calculation





st.title("Weekly Salary Calculator")


hourly_wage = float(st.number_input("Hourly Wage", min_value=None, max_value=None, value="min", step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder="min 4.78", disabled=False, label_visibility="visible"))


st.caption("*Enter your weekly working schedule below as 24 hours time format separated by ':' or just simple number format, both are accepted as long as you don't mix both of them for the same day. (e.g. 04:00 or 4, 04:30 or 4.5)*")

d = {'days': ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 'start time': ["","" ,"" ,"" ,"" ,"" ,"" ], 'end time': ["", "", "", "", "", "", ""]}
df = pd.DataFrame(data=d)
edited_df = st.data_editor(df, width="stretch", height="auto", use_container_width=False, hide_index=True, column_order=None, column_config=None, num_rows="fixed", disabled=("col0"), key=None, on_change=None, args=None, kwargs=None)


monday = Regular("Monday",0,0,0)
tuesday = Regular("Tuesday",0,0,0)
wednesday = Regular("Wednesday",0,0,0)
thursday = Regular("Thursday",0,0,0)
friday = Regular("Friday",0,0,0)
saturday = Regular("Saturday",0,0,0)
sunday = Bonus("Sunday", 0, 0, 0)
monday_extra = Regular("MondayExtra",0,0,0)

days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday, monday_extra]


def calculate_period_hours(format ,start_time, end_time):
    # Convert times to hours (e.g., 6:30 -> 6.5)

    if format == "time":
        start_hour = int(start_time.split(':')[0]) + int(start_time.split(':')[1]) / 60
        end_hour = int(end_time.split(':')[0]) + int(end_time.split(':')[1]) / 60
    else:
        start_hour = start_time
        end_hour = end_time
    # Handle overnight shifts
    if end_hour < start_hour:
        end_hour += 24

    # Define periods
    period1_start, period1_end = 6, 22
    period2_start, period2_end = 22, 24
    period3_start, period3_end = 0, 6

    period1_hours = 0
    period2_hours = 0
    period3_hours = 0

    # Calculate hours for period 1 (06:00 - 22:00)
    if start_hour < period1_end and end_hour > period1_start:
        period1_hours = min(end_hour, period1_end) - max(start_hour, period1_start)
        period1_hours = max(0, period1_hours)

    # Calculate hours for period 2 (22:00 - 24:00)
    if start_hour < period2_end and end_hour > period2_start:
        period2_hours = min(end_hour, period2_end) - max(start_hour, period2_start)
        period2_hours = max(0, period2_hours)

    # Calculate hours for period 3 (00:00 - 06:00)
    if start_hour < 24 and end_hour > 24:
        period3_hours = min(end_hour - 24, period3_end) - max(start_hour - 24, period3_start)
        period3_hours = max(0, period3_hours)
    elif start_hour < period3_end and end_hour > period3_start:
        period3_hours = min(end_hour, period3_end) - max(start_hour, period3_start)
        period3_hours = max(0, period3_hours)

    return period1_hours, period2_hours, period3_hours



def calculate():
    for i in range(7):
        start = str(edited_df["start time"].get(i))
        end = str(edited_df["end time"].get(i))

        if start and end:
            if ":" in start or ":" in end:
                days[i].period1, days[i].period2, days[i + 1].period3 = calculate_period_hours(
                    "time", start, end)
            else:
                days[i].period1, days[i].period2, days[i + 1].period3 = calculate_period_hours(
                    "int", float(start), float(end))

    total_value = 0
    for day in days:
        day.calculate()
        total_value = total_value + day.calculated_wage

    weekly_wage = total_value * hourly_wage

    return f"Weekly Wage: €{weekly_wage:.2f}"


try:
    if st.button("Calculate"):
        st.subheader(calculate())

        st.caption("-Overtime and holiday (other than Sundays) working can not be calculated yet with this program. ")
        st.caption("-In the case your working time is not continuous in a day and you want to calculate your "
                 "weekly salary with more than one shift for the same day, it is not automatically supported yet. But "
                 "still you can fill as many as form you wish and make calculation for every different shift of you, "
                 "then you can summarize them manually.")

except IndexError:
    st.write("Error! You must enter the time value in the same and right format for each row of the table. Choose "
             "only one format as time (19:00 or 19:30) or number (19 or 19.5) for a line. ")

except ValueError:
    st.write("Error! You must enter the time value in the right format. Choose a valid format as time (19:00 or "
             "19:30) or number (19 or 19.5), do not use any other letter or character. ")


