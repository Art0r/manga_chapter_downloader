import re

def slugify(input_string):
    # Convert to lowercase and replace spaces with hyphens
    slug = input_string.lower().replace(" ", "-")
    
    # Remove non-alphanumeric characters and hyphens that occur consecutively
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', slug)
    
    # Remove leading and trailing hyphens
    slug = slug.strip('-')
    
    return slug
