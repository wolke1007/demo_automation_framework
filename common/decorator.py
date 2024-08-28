from functools import wraps
from PIL import Image
from io import BytesIO
import allure


def capture_screenshot_after_step(func):
    """
    To attach screenshot in allure report when finish a single step
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        driver = args[0].driver  # Assuming `self.driver` is available in the context
        page_obj = args[0]  # Assuming `self.driver` is available in the context
        if driver.__class__.__module__.startswith('selenium'):
            page_obj.is_page_all_pic_loaded()
            # if allure report step screenshot timing is wrong, try to add stability_time,
            # but that reduce test efficiency
            page_obj.wait_for_dom_stability(stability_time=1)
            screenshot = driver.get_screenshot_as_png()
        elif driver.__class__.__module__.startswith('appium'):
            screenshot = driver.get_screenshot_as_png()
        else:
            raise RuntimeError("page_obj type wrong")
        # Resize the screenshot based on a ratio
        image = Image.open(BytesIO(screenshot))
        width, height = image.size

        ratio = 1 / 3  # or 1/3, etc.
        new_width = int(width * ratio)
        new_height = int(height * ratio)

        resized_image = image.resize((new_width, new_height))
        buffer = BytesIO()
        resized_image.save(buffer, format="PNG")
        resized_screenshot = buffer.getvalue()

        # Infer the step name from the function name
        func_name = func.__name__.replace("_", " ").title()
        allure.attach(resized_screenshot, name=f"{func_name} Screenshot", attachment_type=allure.attachment_type.PNG)
        return result

    return wrapper
