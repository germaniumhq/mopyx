
def _is_displayed_filter(item):
    try:
        result = item.is_displayed()

        #print("is_displayed? %s" % result)
        return True

        #return result
    except Exception as e:
        print(e)
        return False
