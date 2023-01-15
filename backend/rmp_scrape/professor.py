class Professor:
    """
    professor class to classify professor information
    """
    def __init__(self, ratemyprof_id: int, first_name: str, last_name: str, num_of_ratings: int, overall_rating, rating_class: str, department: str):
        # differentiate between two seeds from RMP
        self.ratemyprof_id = ratemyprof_id

        # get professor basic information
        self.name = f"{first_name} {last_name}"
        self.first_name = first_name
        self.last_name = last_name
        self.num_of_ratings = num_of_ratings
        self.rating_class = rating_class
        self.department = department

        # get rating for professor
        if self.num_of_ratings < 1:
            self.overall_rating = 0

        else:
            self.overall_rating = float(overall_rating)