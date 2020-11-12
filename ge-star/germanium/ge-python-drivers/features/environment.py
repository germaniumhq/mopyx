

def after_scenario(context, scenario):
    if 'browser' in context:
        context.browser.quit()
