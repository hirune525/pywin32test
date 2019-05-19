import ctypes

BM_CLICK = 0x00F5

user32 = ctypes.WinDLL('user32')

EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
EnumChildWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

user32.EnumWindows.restype = ctypes.c_bool
user32.EnumWindows.argtypes = (EnumWindowsProc, ctypes.c_void_p)

user32.EnumChildWindows.restype = ctypes.c_bool
user32.EnumChildWindows.argtypes = (ctypes.c_int, EnumChildWindowsProc, ctypes.c_void_p)    

user32.GetWindowTextW.restype = ctypes.c_int
user32.GetWindowTextW.argtypes = (ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int)

user32.GetClassNameW.restype = ctypes.c_int
user32.GetClassNameW.argtypes = (ctypes.c_int, ctypes.c_wchar_p, ctypes.c_int)

user32.SendMessageW.restype = ctypes.c_void_p #ctypes.POINTER(ctypes.c_long)
user32.SendMessageW.argtypes = (ctypes.c_int, ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p)

def get_parent_windows():
    windows = []
    def callback(hWnd, lParam):
        windowText = ctypes.create_unicode_buffer(1024)
        user32.GetWindowTextW(hWnd, windowText, len(windowText))
        className = ctypes.create_unicode_buffer(1024)
        user32.GetClassNameW(hWnd, className, len(className))
        windows.append((hWnd, windowText.value, className.value))
        return True

    user32.EnumWindows(EnumWindowsProc(callback), None)
    return windows

def get_child_windows(parendHWND):
    child_windows = []
    def callback(hWnd, lParam):
        windowText = ctypes.create_unicode_buffer(1024)
        user32.GetWindowTextW(hWnd, windowText, len(windowText))
        className = ctypes.create_unicode_buffer(1024)
        user32.GetClassNameW(hWnd, className, len(className))
        child_windows.append((hWnd, windowText.value, className.value))
        return True
    
    user32.EnumChildWindows(parendHWND, EnumChildWindowsProc(callback), None)
    return child_windows

def main():
    
    parent_windows = get_parent_windows()

    for parent_window in parent_windows:
        # print(parent_window)
        # if parent_window[1] == 'ダウンロードの表示 - Internet Explorer':
        # if 'Internet Explorer' in parent_window[1]:
        # if 'Python Release Python 3.7.3 | Python.org - Internet Explorer' == parent_window[1] and 'IEFrame' == parent_window[2]:
        if 'Python Release Python 3.7.3 | Python.org - Internet Explorer' == parent_window[1] and 'TabThumbnailWindow' == parent_window[2]:
            #print('find')TabThumbnailWindow
            print(parent_window)
            # child_item = parent_window
            target_window = parent_window
            break
    
    print('-----------------')

    def temp(window_item):
        print(window_item)
        # user32.SendMessageW(window_item[0], BM_CLICK, 0, 0)

        child_windows = get_child_windows(window_item[0])
        if bool(child_windows):
            for child_window in child_windows:
                temp(child_window)
                print('-----------------')
        else:
            return

    temp(target_window)

    # notify_bar = None
    # for child_window in child_windows:
    #     print(child_window)
    #     if child_window[2] == 'DirectUIHWND':
    #         notify_bar = child_window

    # print('-----------------')


if __name__ == "__main__":
    main()
