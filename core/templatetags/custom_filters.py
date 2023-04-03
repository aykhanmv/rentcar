from django import template

register = template.Library()

@register.filter(name='limit_images')
def limit_images(images, num):
    return images[:num]
