from django import template

register = template.Library()

# مپ ارقام فارسی به انگلیسی
persian_digits = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")

@register.filter
def three_digits(value):
    try:
        # تبدیل ورودی به رشته، تبدیل ارقام فارسی به انگلیسی، حذف کاما یا جداکننده‌های احتمالی
        val_str = str(value).translate(persian_digits).replace(',', '').replace('٬', '').replace('٫', '')
        number = int(val_str)
        # فرمت با جداکننده کاما، سپس تبدیل کاما به نقطه
        formatted = f"{number:,}".replace(',', '.')
        return formatted
    except (ValueError, TypeError):
        return value
