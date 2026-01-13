
def test1():
    try:
        button_link = "frwrgregregrege"
        if not button_link.startswith("http://") or not button_link.startswith("https://"):
            # If validation fails, return an error payload
            print("Invalid URL")
    except Exception as e:
        print(f"Exception occurred: {e}") 

def test2():
    try:
        some_list = [1]
        if not some_list:
            print("is empyty")
        else:
            print("List is not empty")
    except Exception as e:
        print(f"Exception occurred: {e}")


def test3():
    value = {"key1": "value1", "key2": "value2"}
    something = value.get("call_to_action_dropdown")

    if something and something.get("selected_option"):
        try:
            print("Key exists")
        except Exception as e:
            print(f"Exception occurred: {e}")
    
    print("Key does not exist")

test3()
  

