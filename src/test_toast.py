# Test the toast module to make sure you can receive
# toast notifications in your given environment (Windows only)

from win10toast import ToastNotifier


def show_notification():
    toaster = ToastNotifier()
    toaster.show_toast("Test Notification", "This is a test notification", duration=10)
    if toaster:
        return 0
    else:
        print("There was an error initializing ToastNotifier()")
        return 1


def main():
    show_notification()


if __name__ == "__main__":
    main()
