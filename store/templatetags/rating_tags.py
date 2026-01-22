from django import template

register = template.Library()

@register.filter
def get_rating_stars(rating):
    """
    Returns HTML for displaying star rating
    rating: float value between 0 and 5
    Returns: HTML string with full stars, half stars, and empty stars
    """
    if rating is None:
        rating = 0
    
    rating = float(rating)
    full_stars = int(rating)
    has_half_star = (rating - full_stars) >= 0.5
    empty_stars = 5 - full_stars - (1 if has_half_star else 0)
    
    html = '<div class="rating-display">'
    
    # Full stars
    for i in range(full_stars):
        html += '<i class="fa fa-star"></i>'
    
    # Half star
    if has_half_star:
        html += '<i class="fa fa-star-half-o"></i>'
    
    # Empty stars
    for i in range(empty_stars):
        html += '<i class="fa fa-star-o"></i>'
    
    html += '</div>'
    return html
