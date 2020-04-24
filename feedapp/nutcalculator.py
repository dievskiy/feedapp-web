class NutrientCalculator:

    def __init__(self):
        # tags for each nutrient

        self.tag_calories = 'consumedCalories'
        self.tag_proteins = 'consumedProtein'
        self.tag_fat = 'consumedFat'
        self.tag_carbs = 'consumedCarbs'

    # return dictionary of days with corresponding nutrient values
    def count_nutrient(self, days):
        days_d = {}
        try:
            if not (days is None or len(days) == 0):
                for day in days:
                    total_calories = 0.0
                    total_proteins = 0.0
                    total_fats = 0.0
                    total_carbs = 0.0
                    for meal in day['meals']:
                        for product in meal['products']:
                            total_calories += product[self.tag_calories]
                            total_proteins += product[self.tag_proteins]
                            total_fats += product[self.tag_fat]
                            total_carbs += product[self.tag_carbs]
                    days_d[day['date']['day']] = {'calories': total_calories, 'proteins': total_proteins,
                                                  'fats': total_fats,
                                                  'carbs': total_carbs}
        except:
            pass

        return days_d
