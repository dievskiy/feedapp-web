class NutrientCalculator:

    def __init__(self):
        # tags for each nutrient

        self.tag_calories = 'consumedCalories'
        self.tag_proteins = 'consumedProtein'
        self.tag_fat = 'consumedFat'
        self.tag_carbs = 'consumedCarbs'

    def count_nutrients(self, days):
        """
        Counts total nutrients from all days
        :param days:
        :return: dictionary of days with corresponding nutrient values
        """
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


class NutrientsPlotter:

    def __init__(self, days):
        self.days = days

    def get_encoded_images_bytes(self):
        from io import BytesIO
        from PIL import Image
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')
        import base64
        import numpy as np

        # set up plot figure to display properly
        days_names = []
        calories = []
        proteins = []
        carbs = []
        fats = []

        for k, v in self.days.items():
            calories.append(int(v['calories']))
            proteins.append(int(v['proteins']))
            carbs.append(int(v['carbs']))
            fats.append(int(v['fats']))
            days_names.append(k)

        n = np.arange(len(self.days.keys()))
        fig = plt.figure(num=0, figsize=(10, 5), dpi=100)
        plt.clf()
        fig.suptitle('Calories', fontsize=18)
        plt.xlabel('Days')
        plt.ylabel('Calories')
        plt.bar(n, height=calories, color="#71adf2")

        # set correct x-axis labels
        plt.xticks(n, days_names)

        # save calories image
        # save image as bytes
        calories_image = BytesIO()
        plt.savefig(calories_image, format='png')
        calories_image.seek(0)
        calories_image_bytes = base64.b64encode(calories_image.getvalue())

        # save other nutrient image
        fig2 = plt.figure(num=1, figsize=(10, 5), dpi=100)
        plt.clf()
        fig2.suptitle('Proteins, Carbs and Fats', fontsize=18)
        plt.plot(proteins, '-r', label='proteins', color="#f7c443")
        plt.plot(carbs, '-b', label='carbs', color="#71adf2")
        plt.plot(fats, '-g', label='fats')
        plt.xlabel('Days')
        plt.ylabel('Grams')
        plt.legend(loc="upper left")
        plt.xticks(n, days_names)

        other_nutrients_image = BytesIO()
        plt.savefig(other_nutrients_image, format='png')
        other_nutrients_image.seek(0)
        other_nutrients_image_bytes = base64.b64encode(other_nutrients_image.getvalue())

        return calories_image_bytes, other_nutrients_image_bytes
