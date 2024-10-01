from rest_framework.throttling import UserRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'  # This is the name of the throttle
    # rate = '10/minute'  # This is the rate limit (requests per minute)
    # duration = 60  # This is the duration for the rate limit (in seconds)
    
class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'  # This is the name of the throttle
    # rate = '10/minute'  # This is the rate limit (requests per minute)
    # duration = 60  # This is the duration for the rate limit (in seconds)
    