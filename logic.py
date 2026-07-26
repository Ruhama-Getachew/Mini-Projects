from datetime import date

def get_day_name(day, month, year, calendar_type):
    if calendar_type == "E.C.":
        ethiopian = EthiopianCalendar(day, month, year)
        return ethiopian.required_date

    elif calendar_type == "G.C.":
        gregorian = ConvertCalendar(year, month, day)
        ethiopian = EthiopianCalendar(
            gregorian.conv_day,
            gregorian.conv_month,
            gregorian.conv_year
        )
        return ethiopian.required_date

    return "Invalid input"


class EthiopianCalendar:
    def __init__(self, et_day, et_month, et_year):
        self.year = et_year
        self.month = et_month
        self.day = et_day
        self.ethiopian_holiday = self.ethiopian_holiday()
        self.early_wednesday = self.early_wednesday()
        self.required_date = self.required_date()

    def ethiopian_holiday(self):
        Total_year = 5500 + self.year
        rabbit_amount = int(Total_year / 4)
        day_remainder = (Total_year + rabbit_amount) % 7
        holiday_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday"]
        for num in range(0, 8):
            if num == day_remainder:
                return holiday_list[num]
            else:
                pass
        return None

    def early_wednesday(self):
        wednesday_list = ["None", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday"]
        if self.ethiopian_holiday in wednesday_list:
            return wednesday_list.index(self.ethiopian_holiday)
        return None

    def required_date(self):
        add = self.early_wednesday + (2 * self.month) + self.day
        required_day_remainder = add % 7
        final_day_list = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        for num in range(0, 8):
            if num == required_day_remainder:
                return f'It is on "{final_day_list[num]}".'
            else:
                pass
        return None


class ConvertCalendar:
    def __init__(self, g_year, g_month, g_day):
        self.day = g_day
        self.month = g_month
        self.year = g_year
        self.conv_day, self.conv_month, self.conv_year = self.gregorian_to_ethiopian()

    @staticmethod
    def is_leap_year(year):
        # year = self.year
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def gregorian_to_ethiopian(self):
        g_date = date(self.year, self.month, self.day)

        # Determine Ethiopian New Year in Gregorian
        if self.is_leap_year(self.year):
            new_year = date(self.year, 9, 12)
        else:
            new_year = date(self.year, 9, 11)

        # Step 1: Determine Ethiopian year
        if g_date >= new_year:
            e_year = self.year - 7
            start_year = new_year
        else:
            e_year = self.year - 8
            # previous Ethiopian new year
            if self.is_leap_year(self.year - 1):
                start_year = date(self.year - 1, 9, 12)
            else:
                start_year = date(self.year - 1, 9, 11)

        # Step 2: Calculate number of days since Ethiopian New Year
        delta_days = (g_date - start_year).days

        # Step 3: Ethiopian month and day
        e_month = delta_days // 30 + 1
        e_day = delta_days % 30 + 1

        return e_day, e_month, e_year
